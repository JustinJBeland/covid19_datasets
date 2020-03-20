import pandas as pd
import io
import requests
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import numpy as np 
import subprocess
import os



def make_gif(case_type='confirmed'):

    BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
    if case_type == 'confirmed':
        SUB_URL = 'time_series_19-covid-Confirmed.csv'
        color = 'red'
    elif case_type == 'deaths':
        SUB_URL = 'time_series_19-covid-Deaths.csv'
        color = 'darkred'
    elif case_type == 'recovered':
        SUB_URL = 'time_series_19-covid-Recovered.csv'
        color = 'green'

    # load csse datasets
    case_data = pd.read_csv(io.StringIO(requests.get(BASE_URL+SUB_URL).content.decode('utf-8')))



    n_timepoints = case_data.shape[1]


    for time in range(4,n_timepoints):

        # create new figure, axes instances.
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])

        m = Basemap(projection='mill')

        m.drawcoastlines()
        m.fillcontinents()
        m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
        m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])

        for prov_state in range(len(case_data)):
            lat = case_data.iloc[prov_state][2]
            lon = case_data.iloc[prov_state][3]

            num_cases = case_data.iloc[prov_state][time]
            if num_cases == 0:
                num_cases = 1e-8

            size = np.log(num_cases)+1


            x, y = m(lon,lat)
            m.plot(x,y, 'o',color=color,markersize=size, alpha=0.3)


        ax.set_title(case_type + ' ' + case_data.columns.values[time] + ' (log scale)')
        plt.savefig(str(time).zfill(4))



    i='*.png'
    o = case_type + '.gif'
    subprocess.call("convert -delay 30 -loop 5 " + i + " " + o, shell=True)



make_gif('confirmed')
make_gif('deaths')
make_gif('recovered')


# delete figures
origfolder = os.getcwd()
test = os.listdir(origfolder)

for item in test:
    if item.endswith(".png"):
        os.remove(os.path.join(origfolder, item))
























