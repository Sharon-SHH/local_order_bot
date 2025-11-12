class OrderMerge:
    @staticmethod
    def merge(cart, new_draft):
        # 合并 items
        for new_item in new_draft.items:
            matched = False
            for existing_item in cart.items:
                if (existing_item.category == new_item.category and
                    existing_item.name == new_item.name and
                    existing_item.size == new_item.size and
                    set(existing_item.toppings) == set(new_item.toppings)):
                    existing_item.qty += new_item.qty
                    matched = True
                    break
            if not matched:
                cart.items.append(new_item)

        # 如果之前没有 service/address/notes，就从新单补上
        if not cart.service and new_draft.service:
            cart.service = new_draft.service
        if not cart.address and new_draft.address:
            cart.address = new_draft.address
        if not cart.notes and new_draft.notes:
            cart.notes = new_draft.notes

        return cart
