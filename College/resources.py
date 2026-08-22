from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from Auth.models import CollegeAdmin
from General.models import CollegeType, OrganizationType
from .models import College


class CollegeResource(resources.ModelResource):
    """
    Excel/CSV import for colleges.
    Required column: college_user (College User email, e.g. demo1@college.com)
    Also required: name, organization_type, college_type, rank, established_year, overview, city
    """
    college_user = fields.Field(
        column_name='college_user',
        attribute='college_user',
        widget=ForeignKeyWidget(CollegeAdmin, 'email'),
    )
    organization_type = fields.Field(
        column_name='organization_type',
        attribute='organization_type',
        widget=ForeignKeyWidget(OrganizationType, 'name'),
    )
    college_type = fields.Field(
        column_name='college_type',
        attribute='college_type',
        widget=ForeignKeyWidget(CollegeType, 'name'),
    )

    class Meta:
        model = College
        import_id_fields = ('name',)
        skip_unchanged = True
        report_skipped = True
        fields = (
            'college_user',
            'name',
            'affiliation',
            'organization_type',
            'college_type',
            'rank',
            'rating',
            'established_year',
            'overview',
            'city',
            'primary_mobile',
            'email',
            'website',
            'meta_title',
            'slug',
        )
        exclude = (
            'logo',
            'image',
            'course_category',
            'course_subcategory',
            'admission_process',
            'specialization',
            'career_opportunity',
            'placement',
            'scholarship',
            'scope',
            'views',
            'created_at',
            'updated_at',
        )
