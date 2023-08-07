from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
from json import dumps


indicators = pd.read_csv('D:\Virtual_Desktop\Galantis\StonyBrookUniversity\/16_CourseWork\Sem2\/2_Vis\FinalProject\Dataset\wdi-csv-zip-57-mb-\WDIData.csv').drop(columns='Unnamed: 63')

# Create your views here.
def homepage(request):
    acc_electrictiy, acc_electrictiy_ru, acc_electrictiy_ur = worldwide_electricity()
    energy = worldwide_energy()
    pcpData = pcpData_generate()
    barplotData = barData_generate()
    fossilmix = fossil_generate()
    return render(request, 'myapp/homepage.html', {'context':{'world_electricity': dumps(acc_electrictiy), 'world_electricity_ru': dumps(acc_electrictiy_ru),
                                                              'world_electricity_ur': dumps(acc_electrictiy_ur), 'world_energy': dumps(energy),
                                                              'pcp_data': dumps(pcpData), 'bar_plot_data': dumps(barplotData), 'piedata': dumps(fossilmix)}})



def barData_generate():
    my_renew_adoption = pd.DataFrame()

    renew_adoption = indicators[indicators['Indicator Code']=='EG.ELC.RNWX.ZS']
    my_renew_adoption = my_renew_adoption.append(renew_adoption, ignore_index=False)

    my_renew_dict = {}
    for year in range(1960, 2019):
        temp_list = []
        for idx, row in my_renew_adoption.iterrows():
            val = 0
            if str(row[str(year)]) != 'nan':
                val = str(row[str(year)])
            temp_list.append({'CountryCode': str(row["Country Code"]), 'value': val})
        sorted_list = sorted(temp_list, key=lambda x: float(x['value']), reverse=True)
        my_renew_dict[str(year)] = sorted_list[:10]

    return my_renew_dict


def worldwide_energy():
    my_fossil = pd.DataFrame()
    my_hydro = pd.DataFrame()
    my_renew = pd.DataFrame()

    fossil = indicators[indicators['Indicator Code']=='EG.ELC.FOSL.ZS']
    hydro = indicators[indicators['Indicator Code']=='EG.ELC.HYRO.ZS']
    renew = indicators[indicators['Indicator Code']=='EG.ELC.RNWX.ZS']

    my_fossil = my_fossil.append(fossil, ignore_index=False)
    my_hydro = my_hydro.append(hydro, ignore_index=False)
    my_renew = my_renew.append(renew, ignore_index=False)

    print(len(my_fossil), len(my_hydro), len(my_renew))

    my_energy_dict = []

    for i in range(len(my_fossil)):
        for year in range(1960, 2019):
            temp_dict = {}
            temp_dict['year'] = year
            temp_dict['Country'] = my_fossil.iloc[i, 0]
            temp_dict['Countrycode'] = my_fossil.iloc[i, 1]

            if str(my_fossil.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['Fossil'] = str(0)
            else:
                temp_dict['Fossil'] = str(my_fossil.iloc[i, 4+(year-1960)])

            if str(my_hydro.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['Hydro'] = str(0)
            else:
                temp_dict['Hydro'] = str(my_hydro.iloc[i, 4+(year-1960)])

            if str(my_renew.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['Renew'] = str(0)
            else:
                temp_dict['Renew'] = str(my_renew.iloc[i, 4+(year-1960)])

            if temp_dict['Fossil'] == str(0) and temp_dict['Hydro'] == str(0) and temp_dict['Renew'] == str(0):
                continue
            else:
                my_energy_dict.append(temp_dict)

    return my_energy_dict



def fossil_generate():
    my_gas = pd.DataFrame()
    my_coal = pd.DataFrame()
    my_oil = pd.DataFrame()

    gas = indicators[indicators['Indicator Code']=='EG.ELC.NGAS.ZS']
    coal = indicators[indicators['Indicator Code']=='EG.ELC.COAL.ZS']
    oil = indicators[indicators['Indicator Code']=='EG.ELC.PETR.ZS']

    my_gas = my_gas.append(gas, ignore_index=False)
    my_coal = my_coal.append(coal, ignore_index=False)
    my_oil = my_oil.append(oil, ignore_index=False)

    my_fossil_dist = {}
    

    for i in range(len(my_gas)):
        main_dict = {}
        for year in range(1960, 2019):
            temp_dict = {}
            
            if str(my_gas.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['gas'] = str(0)
            else:
                temp_dict['gas'] = str(my_gas.iloc[i, 4+(year-1960)])

            if str(my_oil.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['oil'] = str(0)
            else:
                temp_dict['oil'] = str(my_oil.iloc[i, 4+(year-1960)])

            if str(my_coal.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['coal'] = str(0)
            else:
                temp_dict['coal'] = str(my_coal.iloc[i, 4+(year-1960)])

            if temp_dict['gas'] == str(0) and temp_dict['oil'] == str(0) and temp_dict['coal'] == str(0):
                continue
            else:
                main_dict[str(year)] = temp_dict

        if main_dict.__len__() !=0 :
            my_fossil_dist[str(my_gas.iloc[i, 1])] = main_dict

    return my_fossil_dist
            



def pcpData_generate():
    fc1 = pd.DataFrame()
    fc2 = pd.DataFrame()
    fc3 = pd.DataFrame()
    fc4 = pd.DataFrame()
    fc5 = pd.DataFrame()

    fc1_data = indicators[(indicators['Indicator Code']=='EN.ATM.CO2E.KD.GD')]
    fc2_data = indicators[(indicators['Indicator Code']=='EG.USE.COMM.CL.ZS')]
    fc3_data = indicators[(indicators['Indicator Code']=='EG.USE.CRNW.ZS')]
    fc4_data = indicators[(indicators['Indicator Code']=='AG.LND.FRST.ZS')]
    fc5_data = indicators[(indicators['Indicator Code']=='EP.PMP.DESL.CD')]

    fc1 = fc1.append(fc1_data, ignore_index=False)
    fc2 = fc2.append(fc2_data, ignore_index=False)
    fc3 = fc3.append(fc3_data, ignore_index=False)
    fc4 = fc4.append(fc4_data, ignore_index=False)
    fc5 = fc5.append(fc5_data, ignore_index=False)

    print(len(fc1), len(fc2), len(fc3), len(fc4), len(fc5) )
    
    my_data = []
    for i in range(len(fc1)):
        for year in range(1960, 2019):
            temp_dict = {}
            temp_dict['year'] = year

            if str(fc1.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['coe'] = 0
            else:
                temp_dict['coe'] = str(fc1.iloc[i, 4+(year-1960)])

            if str(fc2.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['egcom'] = 0
            else:
                temp_dict['egcom'] = str(fc2.iloc[i, 4+(year-1960)])

            if str(fc3.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['combrenew'] = 0
            else: 
                temp_dict['combrenew'] = str(fc3.iloc[i, 4+(year-1960)])
            
            if str(fc4.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['forestarea'] = 0
            else:
                temp_dict['forestarea'] = str(fc4.iloc[i, 4+(year-1960)])

            if str(fc5.iloc[i, 4+(year-1960)]) == 'nan':
                temp_dict['pump'] = 0
            else:
                temp_dict['pump'] = str(fc5.iloc[i, 4+(year-1960)])

            temp_dict['countrycode'] = fc1.iloc[i, 1]

            my_data.append(temp_dict)
        # print(fc2.loc[i, "Country Name"], fc2.loc[i, "Indicator Name"])
    return my_data



def worldwide_electricity():
    df_elec_my = pd.DataFrame()
    df_elec_my_ru = pd.DataFrame()
    df_elec_my_ur = pd.DataFrame()

    df_elec_pop = indicators[(indicators['Indicator Code']=='EG.ELC.ACCS.ZS')]
    df_elec_pop_ru = indicators[(indicators['Indicator Code']=='EG.ELC.ACCS.RU.ZS')]
    df_elec_pop_ur = indicators[(indicators['Indicator Code']=='EG.ELC.ACCS.UR.ZS')]

    df_elec_my = df_elec_my.append(df_elec_pop, ignore_index=False)
    df_elec_my_ru = df_elec_my_ru.append(df_elec_pop_ru, ignore_index=False)
    df_elec_my_ur = df_elec_my_ur.append(df_elec_pop_ur, ignore_index=False)

    df_elec_my.drop(columns=['Country Name', 'Indicator Name', 'Indicator Code'], inplace=True)
    df_elec_my_ru.drop(columns=['Country Name', 'Indicator Name', 'Indicator Code'], inplace=True)
    df_elec_my_ur.drop(columns=['Country Name', 'Indicator Name', 'Indicator Code'], inplace=True)

    
    my_dict = {}
    for index, row in df_elec_my.iterrows():
        temp_dict = []
        for year in range(1960, 2019):
            temp_dict.append(str(row[str(year)]))
        my_dict[row["Country Code"]] = temp_dict

    my_dict_ru = {}
    for index, row in df_elec_my_ru.iterrows():
        temp_dict_ru = []
        for year in range(1960, 2019):
            temp_dict_ru.append(str(row[str(year)]))
        my_dict_ru[row["Country Code"]] = temp_dict_ru

    my_dict_ur = {}
    for index, row in df_elec_my_ur.iterrows():
        temp_dict_ur = []
        for year in range(1960, 2019):
            temp_dict_ur.append(str(row[str(year)]))
        my_dict_ur[row["Country Code"]] = temp_dict_ur

    return my_dict, my_dict_ru, my_dict_ur
    
