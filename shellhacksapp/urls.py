from django.urls import path, include
from . import views as v

app_name = 'shellhacksapp'

urlpatterns = [
    path('', v.hello, name = 'home'),
    path('fetch_financial_data/', v.get_financial_data, name = 'fetch_financial_data'),
    path('google_data/', v.google_data, name='google_data'),
    path('get_company_data/', v.get_company_data, name='get_company_data'),
    path('comparison/', v.comparison_step_one, name='comparison'),
    path('comparison_two/', v.comparison_step_two, name = 'comparison_two'),
    path('comparison_result/', v.comparison_result, name = 'comparison_result'),
    path('comparison_step_two/', v.comparison_step_two, name='comparison_step_two'),

]


