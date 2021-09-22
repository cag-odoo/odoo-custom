# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ModelPathfinderWizard(models.TransientModel):
    _name = "model.pathfinder.wizard"
    _description = "A wizard used to find relations between 2 models"

    start_model_id = fields.Many2one(comodel_name="ir.model")
    start_model_technical_name = fields.Char(related="start_model_id.model")

    end_model_id = fields.Many2one(comodel_name="ir.model", required=True, domain="[('id', '!=', start_model_id)]")
    end_model_technical_name = fields.Char(related="end_model_id.model")

    result_ids = fields.One2many(comodel_name="model.pathfinder.wizard.result", inverse_name="wizard_id")




    def action_find_path(self):
        raw_relations = self.explore_relations()
        clean_relations = self.clean_relations(raw_relations)
        all_paths = self.build_all_paths(clean_relations)

        # Reset of result just in case we launch the script multiple times in the same wizard
        self.result_ids.unlink()

        # Useful for future debugging
        # print("=====================================================")
        # print(" \n".join(["%s" % "".join(["%s => " % model.model for model in path]) for path in all_paths]))
        # print("=====================================================")

        for path in all_paths:
            self.create_result(path)

        action = self.env.ref('odoo_explorer.model_pathfinder_wizard_action').read()[0]
        action['target'] = 'new'
        action['res_id'] = self.id
        return action


    def create_result(self, path):
        m_path = []
        f_path = []
        for i, model in enumerate(path):
            m_path.append(model.model)
            fielded = path[i-1].related_field_from_ids.filtered(lambda f: f.relation == model.model)[:1]
            # print(fielded)
            print("%s => %s" % (model.model, fielded.name))
            f_path.append(path[i-1].related_field_from_ids.filtered(lambda f: f.relation == model.model)[:1].name if i else 'record')

        # Small Bugfix, but I need to understand why sometimes if saved a path that isn't right
        if False in f_path:
            return

        # print("=====================================================")
        # print(f_path)
        # print("=====================================================")

        models_path = " => ".join(m_path)
        fields_path = ".".join(f_path)

        self.env['model.pathfinder.wizard.result'].create({
            'wizard_id': self.id,
            'models_path': models_path,
            'fields_path': fields_path,
        })


    @staticmethod
    def build_all_paths(relations):
        if not relations:
            return []

        paths = [[relations[0]]]
        for i, step_models in enumerate(relations[1:]):
            new_paths = []
            for model in step_models:
                for path in paths:
                    new_path = path + [model]
                    new_paths.append(new_path)
            paths = new_paths

        return paths


    @staticmethod
    def clean_relations(relations):
        for i, models in reversed(list(enumerate(relations[:-1]))):
            link_models = models.filtered(lambda m: set(m.related_field_from_ids.mapped('relation')).intersection(relations[i + 1].mapped('model')))
            relations[i] = link_models

        return relations

    def explore_relations(self):
        # That's our target baby
        target_name = self.end_model_technical_name

        # We init the head node at the start model
        nodes = [self.start_model_id]

        checked_modules = self.env['ir.model']
        model_found = False

        # Arbitrary max depth of 15 (would be weird that we need more)
        while not model_found and len(nodes) < 15:
            models_with_direct_field = self.env['ir.model']
            models_without_direct_field = self.env['ir.model']

            # We take the last depth
            for model in nodes[-1]:
                direct_fields = model.related_field_from_ids.filtered(lambda f: f.relation == target_name)

                if direct_fields:
                    models_with_direct_field += model
                else:
                    models_without_direct_field += model

                checked_modules += model


            if models_with_direct_field:
                # We keep only the models who have a direct relation at the tail of the list
                nodes[-1] = models_with_direct_field
                model_found = True
            else:
                # We can only get the technical of linked models from the related field
                related_models_names = models_without_direct_field.related_field_from_ids.mapped('relation')
                related_models = self.env['ir.model'].search([('model', 'in', related_models_names)])

                # We keep only the models we didn't check
                next_depth_models = related_models - checked_modules

                nodes.append(next_depth_models)

        # We add the target at the end
        nodes.append(self.end_model_id)
        return nodes if model_found else []



class ModelPathfinderWizardResult(models.TransientModel):
    _name = "model.pathfinder.wizard.result"
    _description = "A result entry"

    wizard_id = fields.Many2one(comodel_name="model.pathfinder.wizard")

    models_path = fields.Char()
    fields_path = fields.Char()
