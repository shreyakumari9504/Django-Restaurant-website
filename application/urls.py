from django.urls import path
from django.contrib.auth import views as auth_views
from application import views

urlpatterns = [

    # ======================
    # 🌐 PUBLIC PAGES
    # ======================
    path('', views.home, name='home'),
    path('starterpage.html', views.starterpage, name='starterpage'),
    path('contact.html', views.contact, name='contact'),
    path('form.html', views.form, name='form'),

    # ======================
    # 🔐 AUTH
    # ======================
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # ======================
    # 🔑 PASSWORD RESET
    # ======================
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='forgot_password.html'
        ),
        name='password_reset'
    ),
    path(
        'reset-done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
    'password-change/',
    auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'
    ),
    name='password_change'
),
path(
    'password-change/done/',
    auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ),
    name='password_change_done'
),


    # ======================
    # 🔁 DASHBOARD ROUTING
    # ======================
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),


    # ======================
    # 👤 USER DASHBOARD
    # ======================
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path(
        'cancel-booking/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),

    # ======================
    # 🛠️ ADMIN DASHBOARD (FULL CRUD)
    # ======================
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

   path(
    'dashboard/booking/add/',
    views.admin_add_booking,
    name='admin_add_booking'
),
path(
    'dashboard/booking/edit/<int:booking_id>/',
    views.admin_edit_booking,
    name='admin_edit_booking'
),
path(
    'dashboard/booking/delete/<int:booking_id>/',
    views.admin_delete_booking,
    name='admin_delete_booking'
),
path(
    'dashboard/booking/cancel/<int:booking_id>/',
    views.admin_cancel_booking,
    name='admin_cancel_booking'
),


    # ======================
    # 🤖 AI
    # ======================
    path("ai-recommend/", views.ai_recommend, name="ai_recommend"),


]
