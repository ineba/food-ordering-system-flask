from datetime import datetime

import constants
from models import Employee, Customer, DeliveryPerson, SQLiteBackend, handle_session


class Controller(SQLiteBackend):
    """ Controller class that inherites from SQLite Backend and 
        composition from Emploeyee, Customer and Delivery Person classes """

    def __init__(self, db_url):
        super(Controller, self).__init__(db_url)
        self.employee = Employee()
        self.customer = Customer()
        self.delivery_person = DeliveryPerson()

    @handle_session
    def add_food_category(self, session, category_name):
        c = self.employee.add_food_category(session, category_name)
        print("\nAdd {}".format("Successfully" if c else "not successfully"))

    @handle_session
    def add_food_details(self, session, category_id, food_name, price):
        d= self.employee.add_food_details(session, category_id, food_name, price)
        print("\nAdd {}".format("Successfully" if d else "not successfully"))

    @handle_session
    def add_delivery_person(self, session, delivery_person_name, delivery_person_phone):
        d = self.employee.add_delivery_person(session, delivery_person_name, delivery_person_phone)
        print("\nAdd {} \nDeliver person ID: {} ".format(
                "Successfully", d.delivery_person_id if d else  "not successfully"))

    @handle_session
    def assign_deliver_person_to_deliver_order(self, session, order_id, delivery_person_id):
        a = self.employee.assign_deliver_person_to_deliver_order(session, order_id, delivery_person_id) 
        print("\nAdd {}".format("sucessful" if a else "not sucessful")) 

    @handle_session
    def update_order(self, session, order_id, order_status):
        u = self.delivery_person.update_order(session, order_id, order_status) 
        print("Order update {}".format("successful" if u else "not successful"))

    @handle_session
    def view_order_emp(self, session, order_id):
        view_order = self.employee.view_order(session, order_id)
        if view_order:
            for fc, fd, cos in view_order:
                print("\nFood category: {} \nFood name: {} \nFood price: {} \nFood quantity: {} \nPrice per item: {}".format(
                    fc.name, fd.food_name, fd.price, cos.food_qty, (fd.price*cos.food_qty)))
                
    @handle_session
    def view_order_grand_total(self, session, order_id):
        view_order_grand = self.employee.view_order_grand_total(session, order_id)
        if view_order_grand:
            for cd, cosa in view_order_grand:                        
                print("\nCustomer name: {} \nOrder ID: {} \nTotal bill: {}".format(
                    cd.cust_name, cosa.order_id, cosa.bill_amount))                

    @handle_session
    def view_order_status(self, session, order_id):
        view_status = self.employee.view_order_status(session, order_id)
        if view_status:
            for cd, cosa, dp in view_status:
                print("\nCustomer name: {} \nOrder ID: {} \nDeliver person name: {} \nOrder status: {} \nTotal bill: {}".format(
                    cd.cust_name, cosa.order_id, dp.delivery_person_name, cosa.order_status, cosa.bill_amount))

    @handle_session
    def view_revenue_today(self, session, order_status):
        rev_today = self.employee.view_revenue_today(session, order_status)
        if rev_today:
            for ex in rev_today:
                print("\nCustomer name: {} \nOrder ID: {} \nOrder Status: {} \nBill amount: {} \nDate & Time: {}".format(
                    ex.cust_name, ex.order_id, ex.order_status, ex.bill_amount, ex.checkout_time))

    @handle_session
    def sum_revenue_today(self, session, order_status):
        sum_rev_today = self.employee.sum_revenue_today(session, order_status)
        if sum_rev_today:
            for s in sum_rev_today:
                print("\nToday's revenue: {} ".format(s))

    @handle_session
    def delete_order(self, session, order_id):
        d = self.employee.delete_order(session, order_id)
        print("\nOrder delete {}".format("successful" if d else "unsuccessful"))

    @handle_session
    def view_menu(self, session):
        menu = self.customer.view_menu(session)
        for fc, fd in menu:
            print("\nFood ID: {} \nFood category: {} \nFood name: {} \nFood price: {}".format(
                fd.food_id, fc.name, fd.food_name, fd.price))

    @handle_session
    def customer_signup(self, session, cust_name, cust_phone, cust_email):
        c = self.customer.customer_signup(session, cust_name, cust_phone, cust_email)
        if c:
            print("\nSignup {}! Customer ID: {}".format("successfully", c.cust_id if c else "not successfully"))

    @handle_session
    def customer_login(self, session, cust_id):
        login = self.customer.customer_login(session, cust_id)
        return login

    @handle_session
    def process_order(self, session, cust_id):
        o = self.customer.create_order_id(session, cust_id)
        selection = """        
        0. Back
        1. Add food to order
        2. Remove food to order
        3. Update food to order
                
        Select option: 

        """
        option = int(input(selection))

        while option != constants.CUST_OPT_BACK:
            
            if option == constants.CUST_OPT_ADD_FOOD_TO_ORDER:
                food_id = input("Enter food ID: ")
                food_qty = input("Enter food quantity: ")
                a = self.customer.add_food_to_order(session, o.order_id, food_id, food_qty)
                print("Add {}!".format("successful" if a else "not successful."))

            elif option == constants.CUST_OPT_REMOVE_FOOD_TO_ORDER:
                food_id = input("Enter food ID: ")
                r = self.customer.remove_food_to_order(session, o.order_id, food_id)
                print("Items {}".format("removed" if r else "not removed"))

            elif option == constants.CUST_OPT_UPDATE_FOOD_TO_ORDER:
                food_id = input("Enter food ID: ")
                food_qty = input("Enter food quantity: ")
                u = self.customer.update_food_to_order(session, o.order_id, food_id, food_qty)
                print("Items {}".format("updated" if u else "not updated"))

            option = int(input(selection))
        
        if o:
            print("Order {}. \nOrder number: {}".format("generated", o.order_id if o else "not generated"))

    @handle_session
    def view_order(self, session, order_id):
        view_order_item = self.customer.view_order_per_item(session, order_id)
        if view_order_item:
            for fc, fd, cos in view_order_item:
                print("\nFood category: {} \nFood name: {} \nFood price: {} \nFood quantity: {} \nTotal per item: {}".format(
                    fc.name, fd.food_name, fd.price, cos.food_qty, (fd.price*cos.food_qty)))

        view_order_grand = self.customer.view_order_grand_total(session, order_id)
        if view_order_grand:
            for fd, cos, cd, cosa, t in view_order_grand:
                print("\nCustomer name: {} \nOrder ID: {} \nTotal bill: {}".format(cd.cust_name, cosa.order_id, t))

    @handle_session
    def checkout(self, session, order_id, order_status, order_address, checkout_time, estimated_time, bill_amount):
        c = self.customer.checkout(session, order_id, order_status, order_address, 
                        checkout_time, estimated_time, bill_amount) 
        if c:
            print("Checkout {}!".format("successful" if c else "not successful"))

    @handle_session
    def cancel_order(self, session, order_id, order_status):
        c = self.customer.cancel_order(session, order_id, order_status) 
        if c:
            print("Cancel {}!".format("successful" if c else "not successful"))
        
    @handle_session
    def view_orders_status(self, session, order_id):
        view_order_item = self.customer.view_order_per_item(session, order_id)
        if view_order_item:
            for fc, fd, cos in view_order_item:
                print("\nFood category: {} \nFood name: {} \nFood price: {} \nFood quantity: {} \nTotal per item: {}".format(
                    fc.name, fd.food_name, fd.price, cos.food_qty, (fd.price*cos.food_qty)))
                        
        view_status = self.customer.view_orders_status(session, order_id)
        if view_status:
            for cos, cd, cosa, dp in view_status:                        
                print("\nCustomer name: {} \nOrder ID: {} \nDeliver person name: {} \nOrder status: {} \nTotal price: {}".format(
                    cd.cust_name, cosa.order_id, dp.delivery_person_name, cosa.order_status, cosa.bill_amount))