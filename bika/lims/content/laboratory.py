from DateTime import DateTime
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ListFolderContents, \
    ModifyPortalContent, View
from plone.app import folder
from Products.Archetypes.public import *
from bika.lims.content.organisation import Organisation
from bika.lims.config import ManageBika, PROJECTNAME
from bika.lims import bikaMessageFactory as _

schema = Organisation.schema.copy() + Schema((
    IntegerField('Confidence',
        schemata = 'Accreditation',
        widget = IntegerWidget(
            label = _("Confidence Level %"),
            description = _("Confidence Level % description",
                            "This value is reported at the bottom of all published results"),
        ),
    ),
    StringField('LabURL',
        schemata = 'Address',
        write_permission = ManageBika,
        widget = StringWidget(
            size = 60,
            label = _("Lab URL"),
            description = _("Lab URL description",
                            "The Laboratory's web address"),
        ),
    ),
    BooleanField('LaboratoryAccredited',
        default = False,
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = BooleanWidget(
            label = _("Laboratory Accredited"),
            description = _("Laboratory Accredited description",
                            "Check this box if your laboratory is accredited"),
        ),
    ),
    StringField('AccreditationBodyLong',
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = StringWidget(
            size = 60,
            label = _("Accreditation Body"),
            description = _("Accreditation Body description",
                            "The name of the accreditation body corresponding to the abbreviation above, "
                            " e.g. South African National Accreditation Service for SANAS"),
        ),
    ),
    StringField('AccreditationBody',
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = StringWidget(
            label = _("Accreditation Body Abbreviation"),
            description = _("Accreditation Body Abbreviation description",
                            "E.g. SANAS, APLAC, etc."),
        ),
    ),
    StringField('AccreditationBodyURL',
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = StringWidget(
            label = _("Accreditation Body URL"),
            description = _("Accreditation Body URL description",
                            "Web address for the accreditation body"),
        ),
    ),
    StringField('Accreditation',
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = StringWidget(
            label = _("Accreditation"),
            description = _("Accreditation Description",
                            "The accreditation standard that applies, e.g. ISO 17025"),
        ),
    ),
    StringField('AccreditationReference',
        schemata = 'Accreditation',
        write_permission = ManageBika,
        widget = StringWidget(
            label = _("Accreditation Reference"),
            description = _("Accreditation Reference description",
                            "The reference code issued to the lab by the accreditation body"),
        ),
    ),
    ImageField('AccreditationBodyLogo',
        schemata = 'Accreditation',
        widget = ImageWidget(
            label = _("Accreditation Logo"),
            description = _("Accreditation Logo descr",
                            "Please upload the logo you are authorised to use on your "
                            "website and results reports by your accreditation body. "
                            "Maximum size is 175 x 175 pixels.")
        ),
    ),
))

IdField = schema['id']
IdField.widget.visible = {'edit':'hidden', 'view': 'invisible'}

schema['Name'].validators = ()
# Update the validation layer after change the validator in runtime
schema['Name']._validationLayer()

class Laboratory(UniqueObject, Organisation):
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    security.declareProtected(View, 'getSchema')
    def getSchema(self):
        return self.schema

registerType(Laboratory, PROJECTNAME)
