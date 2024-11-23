## Uk VersitionL 1.0.0



**Api list:**
### Accounts
#### Models: UserModel, UserProfile
1. auth/register
2. auth/login
3. auth/access_token
4. auth/refresh_token
5. user/profile/
6. user/change_password/
7. user/send_reset_password/<str:uid>/<str:token>/
8. user/<int:pk>/update_profile/ 
9. user/dashboard/

### Supplier
### Models: SupplierProfile
1. supplier/daily_order/
2. supplier/profile/
3. supplier/<int:id>/update_profile/

### Store
#### Models: Card, Menu, Favourite, location 
1. cards/
2. cards/<int:user_id>/favourite/
3. card/<int:pk>/<int:user_id>/add_to_fav/
4. card/purchase/

### Order
#### Models: Payment, Order
1. order/create/<int:card_id>/<int:supp_id>/
2. order/retrieve_by_supplier/<int:supp_id>/
3. order/retrieve_by_card/<int:card_id>/
4. order/retrieve/<int:card_id>/<int:supp_id>/
5. payments/all/


