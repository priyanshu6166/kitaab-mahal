from django.contrib import admin
from .models import Book, Comment, Visitor
from django.utils.html import format_html
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import redirect

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'preview_link')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'cover_image')
        }),
        ('Book Content', {
            'fields': ('pdf_file',),
            'description': 'Upload the PDF file for the book.'
        }),
    )

    def preview_link(self, obj):
        return format_html('<a href="/book/{}/" target="_blank">Preview</a>', obj.id)
    preview_link.short_description = 'Preview Book'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('book__title', 'user__username', 'text')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

class VisitorAdmin(admin.ModelAdmin):
    change_list_template = 'admin/visitor_change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        # Get total unique visitors count
        unique_visitors = Visitor.objects.filter(unique_visitor=True).count()
        
        # Add to context
        if hasattr(response, 'context_data'):
            response.context_data['unique_visitors'] = unique_visitors
            
        return response

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('delete-all/', self.delete_all_visitors, name='delete-all-visitors'),
        ]
        return custom_urls + urls

    def delete_all_visitors(self, request):
        if request.method == 'POST':
            count = Visitor.objects.count()
            Visitor.objects.all().delete()
            messages.success(request, f'Successfully deleted {count} visitors.')
            return redirect('admin:books_visitor_changelist')
        return redirect('admin:books_visitor_changelist')

admin.site.register(Visitor, VisitorAdmin)
admin.site.site_header = "KITAAB MAHAL Admin | Contact: Priyanshukori8171@gmail.com"
admin.site.site_title = "KITAAB MAHAL Admin Portal"
admin.site.index_title = "Welcome to KITAAB MAHAL Admin | Contact: Priyanshukori8171@gmail.com"
