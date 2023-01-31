# -*- coding: utf-8 -*-

#############################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    orientation = fields.Selection([('default', 'Default'), ('left', 'Left'), ('middle', 'Middle'), ('right', 'Right')], string="Orientation")
    background = fields.Selection([('color', 'Color Picker'), ('image', 'Image'), ('url', 'URL')], string="Background")
    image = fields.Binary(string="Image")
    url = fields.Char(string="URL")
    color = fields.Char(string="Color")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            background=params.get_param('masters.background'),
            orientation=params.get_param('masters.orientation'),
            image=params.get_param('masters.image'),
            url=params.get_param('masters.url'),
            color=params.get_param('masters.color'),
        )

        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        set_orientation = self.orientation or False
        set_image = self.image or False
        set_url = self.url or False
        set_color = self.color or False
        set_background = self.background or False
        params.set_param('masters.background', set_background)
        params.set_param('masters.orientation', set_orientation)
        params.set_param('masters.image', set_image)
        params.set_param('masters.url', set_url)
        params.set_param('masters.color', set_color)

    @api.onchange('orientation')
    def onchange_orientation(self):
        if self.orientation == 'default':
            self.background = False
