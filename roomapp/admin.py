from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Customer, Additional_id, Grouped_room, Room, Booked,
    Advance_payment, Customer_list, Ch_out, Order, Non_room_user
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',  'phone_number', 
         'check_in', 'check_out', 'total_room_cost', 
        'total_advance_payment', 'remaining_balance'
    )
    search_fields = ('full_name', 'phone_number', 'passport_id_number')
    list_filter = ('nationality', 'check_in', 'check_out')
    readonly_fields = ('total_room_cost', 'total_advance_payment', 'remaining_balance')

    def total_room_cost(self, obj):
        return obj.total_room_cost
    total_room_cost.short_description = 'Total Room Cost'

    def total_advance_payment(self, obj):
        return obj.total_advance_payment
    total_advance_payment.short_description = 'Total Advance Payment'

    def remaining_balance(self, obj):
        return obj.remaining_balance
    remaining_balance.short_description = 'Remaining Balance'



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'group', 'price_pernight', 'status')
    search_fields = ('room_number',)
    list_filter = ('status', 'group')





class RoomInline(admin.TabularInline):
    model = Booked.room_id.through
    extra = 1




@admin.register(Advance_payment)
class AdvancePaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'Advance_amount', 'payment_mode', 'payment_day')
    search_fields = ('customer__full_name',)
    list_filter = ('payment_mode', 'payment_day')


@admin.register(Customer_list)
class CustomerListAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'checkin', 'checkout', 'total_amount')
    search_fields = ('customer__full_name',)
    list_filter = ('status', 'checkin')
    readonly_fields = ('total_amount', 'total_resturent_amount', 'room_cost', 'all_rooms')

    def total_amount(self, obj):
        return obj.total_amount
    total_amount.short_description = 'Total Advance Payment'

    def total_resturent_amount(self, obj):
        return obj.total_resturent_amount
    total_resturent_amount.short_description = 'Total Restaurant Expense'

    def room_cost(self, obj):
        return obj.room_cost
    room_cost.short_description = 'Room Cost'

    def all_rooms(self, obj):
        return ", ".join([str(room) for room in obj.all_rooms])
    all_rooms.short_description = 'Booked Rooms'





@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'room', 'total', 'order_date')
    search_fields = ('order_id', 'customer__full_name')
    list_filter = ('order_date',)


@admin.register(Non_room_user)
class NonRoomUserAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'full_name', 'phone_number', 'total', 'remaing_amount', 'Payment_mode', 'order_date')
    search_fields = ('order_id', 'full_name', 'phone_number')
    list_filter = ('Payment_mode', 'order_date')



