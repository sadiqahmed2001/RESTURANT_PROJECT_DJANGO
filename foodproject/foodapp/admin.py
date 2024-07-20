from django.contrib import admin
from .models import Post,TeamMember,Reservation,Testimonial,ContactForm,MenuItem,Cart,Order,Payment

# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    list_filter = ['status', 'publish', 'created', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['-publish']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation']
    list_filter = ['designation']
    search_fields = ['full_name', 'designation']
    ordering = ['full_name']
    show_facets = admin.ShowFacets.ALWAYS  # Custom functionality, if applicable

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_time', 'num_people', 'special_request', 'is_reserved','created_at', 'updated_at')
    list_filter = ('date_time', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_reserved', 'mark_as_Waiting']
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'date_time', 'num_people', 'special_request','is_reserved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    def mark_as_reserved(self, request, queryset):
        queryset.update(is_reserved=True)
    mark_as_reserved.short_description = "Mark selected queries as reserved"

    def mark_as_notreserved(self, request, queryset):
        queryset.update(is_waiting=False)
    mark_as_notreserved.short_description = "Mark selected queries as on waiting"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'rating')
    search_fields = ('name', 'profession')
    list_filter = ('rating',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="200" />'
        else:
            return 'No image'
    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_solved', 'created_at')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    actions = ['mark_as_solved', 'mark_as_unsolved']

    def mark_as_solved(self, request, queryset):
        queryset.update(is_solved=True)
    mark_as_solved.short_description = "Mark selected queries as solved"

    def mark_as_unsolved(self, request, queryset):
        queryset.update(is_solved=False)
    mark_as_unsolved.short_description = "Mark selected queries as unsolved"

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'type', 'is_available', 'is_vegetarian')
    list_filter = ('category', 'type', 'is_available', 'is_vegetarian')
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price')
        }),('Category and Type', {'fields': ('category', 'type')}),
        ('Availability', { 'fields': ('is_available', 'is_vegetarian') }),
        ('Image', { 'fields': ('image',)}),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" />'
        else:
            return 'No image'
    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('userid', 'mid', 'qty', 'total_price')
    list_filter = ('userid',)
    search_fields = ('user__username', 'mid__name')

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'm_id', 'qty','is_Paid', 'amt', 'update_desc', 'timestamp')
    list_filter = ('user_id','is_Paid', 'm_id', 'timestamp')
    search_fields = ('order_id', 'update_desc')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    actions = ['mark_as_Ready', 'mark_as_Wait']
    def mark_as_Ready(self, request, queryset):
        queryset.update(is_ready=True)
    mark_as_Ready.short_description = "Mark selected Order Is Ready"

    def mark_as_Wait(self, request, queryset):
        queryset.update(is_Wait=False)
    mark_as_Wait.short_description = "Mark selected Order Is Not Ready Please Wait A moment"

    def mark_as_Paid(self, request, queryset):
        queryset.update(is_ready=True)
    mark_as_Paid.short_description = "Mark As PAid"

    def mark_as_Unpaid(self, request, queryset):
        queryset.update(is_Wait=False)
    mark_as_Unpaid.short_description = "Mark As unpaid"

    def __str__(self):
        return self.order_id


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order', 'payment_method', 'amount', 'is_Paid', 'created_at', 'updated_at')
    list_filter = ('is_Paid', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'order__id', 'rozar_pay_order_id', 'rozar_pay_Payment_id')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Payment, PaymentAdmin)