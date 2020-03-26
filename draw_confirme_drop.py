import plotly.figure_factory as ff
import numpy as np
import pandas as pd
###with adjusted data
def draw_confirm(filename,methods): #
    #filename: for example '03-25-2020.csv'
    #methods: 1 drop no-fips confirmed data.
    #         2 use zip code round methods(not accurate)

    filename = filename
    csvdata = pd.read_csv('./data/{}'.format(filename))
    if methods ==2:
        def fips_confirmed_clean(data):
            data = data.dropna(subset=['Admin2'],how='any')
            try:
                datastaeslist = list(data.Province_State)
                datastaeslist.remove('Wuhan Evacuee')
                data = data[data.Province_State.isin(datastaeslist)]
            except:
                pass
            fip2zip = pd.read_csv('Newver_fips2zip.csv')
            fips_state = pd.read_csv('state_fipslist.csv')
            fips_state_indexstatename = fips_state.set_index('statename')
            fips_standardlist = fip2zip['fip'].to_list()
            fips_standardlist = list(set(fips_standardlist))
            total_df = pd.DataFrame()
            total_df['fips'] = fips_standardlist
            total_df['confirmed'] = np.zeros(len(total_df))
            total_df_indexfips = total_df.set_index('fips')

            use_fips = []
            use_confimation = []
            for i in range(len(data)):
                try:
                    fips = int(data.loc[i]['FIPS'])
                except:
                    fips = np.nan
                confirmdata = data.loc[i]['Confirmed']
                if fips in fips_standardlist:
                    total_df_indexfips.loc[fips]['confirmed'] = confirmdata
            for i in range(len(data)):
                fips = data.loc[i]['FIPS']
                confirmdata = data.loc[i]['Confirmed']
                statename = data.loc[i]['Province_State']
                if fips in fips_standardlist:
                    pass
                else:

                    fips_near_list = fips_state_indexstatename.loc[statename]['fipslist']
                    fips_near_list = eval(fips_near_list)
                    split_confirm = confirmdata/len(fips_near_list)
                    for i in fips_near_list:
                        fipsnum = int(i)
                        total_df_indexfips.loc[fipsnum] = total_df_indexfips.loc[fipsnum].values[0] + split_confirm
            return total_df_indexfips.reset_index()


        df_sample = fips_confirmed_clean(csvdata)
        fip_list = df_sample['fips'].to_list()
        utility_list = df_sample['confirmed'].tolist()
        fip_list_str = []
        for i in fip_list:
            new = str(i)
            if len(new)<5:
                new = '0'*(5-len(new))+new
            fip_list_str.append(new)


        colorscale = ['#ffffff','#ffeff0','#ffdfe0','#ffcfd1','#ffbfc1','#ffafb2','#ff9fa2',
                      '#ff8f93','#ff8083','#ff7074','#ff6064','#ff5055','#ff4045','#ff3036',
                      '#ff2026','#ff1017','#ff0007']


        endpts = list(np.linspace(0, 100, len(colorscale) - 1))
        fips = fip_list_str
        values = utility_list


        fig = ff.create_choropleth(
            fips=fips, values=values, scope=['usa'],
            binning_endpoints=endpts, colorscale=colorscale,
            show_state_data=False,
            show_hover=True,
            asp = 2.9,
            title_text = 'Confirmed Adjusted Data {}'.format(filename),
        )
        fig.layout.template = None
        fig.show()

    if methods==1:
        ###drop no data
        df_sample = csvdata
        df_sample = df_sample.dropna()
        fip_list = df_sample['FIPS'].to_list()
        utility_list = df_sample['Confirmed'].tolist()




        fip_list_str = []
        for i in fip_list:
            new = int(i)
            new = str(new)
            if len(new)<5:
                new = '0'*(5-len(new))+new
            fip_list_str.append(new)


        colorscale = ['#ffffff','#ffeff0','#ffdfe0','#ffcfd1','#ffbfc1','#ffafb2','#ff9fa2',
                      '#ff8f93','#ff8083','#ff7074','#ff6064','#ff5055','#ff4045','#ff3036',
                     '#ff2026','#ff1017','#ff0007'
        ]


        endpts = list(np.linspace(0, 100, len(colorscale) - 1))
        fips = fip_list_str
        values = utility_list


        fig = ff.create_choropleth(
            fips=fips, values=values, scope=['usa'],
            binning_endpoints=endpts, colorscale=colorscale,
            show_state_data=False,
            show_hover=True,
            asp = 2.9,
            title_text = 'Confirmed Drop No Data {}'.format(filename),
        )
        fig.layout.template = None
        fig.show()

draw_confirm('03-25-2020.csv',2)