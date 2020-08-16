
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from data import *
import os, time, glob


def anomaly_det(method,sensor):

    #dat = weekdayData_scaled.reset_index()[['co2_1', 'temp_1', 'dew_1']]
    temp = weekdayData_scaled[['co2_1', 'temp_1', 'dew_1','relH_1']].copy().reset_index()
    
    scaler = StandardScaler()
    temp_scaled = pd.DataFrame(scaler.fit_transform(temp.drop('index',axis=1)))
    
    outliers_fraction = 0.01
    
    if method == "kmeans":
        
        def getDistanceByPoint(data, model):
            distance = list()
            for i in range(0,len(data)):
                Xa = np.array(data.loc[i])
                Xb = model.cluster_centers_[model.labels_[i-1]]
                distance.append(np.linalg.norm(Xa-Xb))
            return distance
        
        n_cluster = range(1, 20)
        sens1 = weekdayData_scaled[[sensor]]
        kmeans = [KMeans(n_clusters=i).fit(sens1) for i in n_cluster]

        model = kmeans[9]
        distance = pd.Series(getDistanceByPoint(temp_scaled, model))
        number_of_outliers = int(outliers_fraction*len(distance))
        threshold = distance.nlargest(number_of_outliers).min()
        threshold_label = (distance >= threshold).astype(int)
        temp['anomaly'] = threshold_label
        a = temp.loc[temp['anomaly'] == 1, ['index', sensor]] #anomaly
        
    elif method == "Iso":
        
        model = IsolationForest(contamination=outliers_fraction).fit(temp_scaled) 
        temp['anomaly'] = pd.Series(model.predict(temp_scaled))
        a = temp.loc[temp['anomaly'] == -1, ['index', sensor]] #anomaly
        
    elif method == "SVM":
        
        model = OneClassSVM(nu=outliers_fraction, kernel="rbf", gamma=0.01).fit(temp_scaled) 
        temp['anomaly'] = pd.Series(model.predict(temp_scaled))
        a = temp.loc[temp['anomaly'] == -1, ['index', sensor]] #anomaly
        
    
    plt.figure(figsize=(10,10))
    plt.plot(temp['index'], temp[sensor], color='blue', label='Normal')
    plt.scatter(a['index'],a[sensor], color='red', label='Anomaly')
    plt.title(method)
    plt.xlabel('Date Time Integer')
    plt.ylabel(sensor + 'sensor')
    plt.legend()


    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)

    plotfile = os.path.join('static/images', str(time.time()) + '.png')
    plt.savefig(plotfile)
    
    return plotfile





if __name__ == '__main__':
    print(anomaly_det("Iso",'co2_1'))