from django.shortcuts import render
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-key': "7c6363ef45msh7ec331a5b277112p19f6dejsn735da244d0d5",
    'x-rapidapi-host': "covid-193.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers).json()


# Create your views here.
def homepage(request):
    noOfResults = int(response['results'])
    countryList = []

    for result in range(0, noOfResults):
        countryList.append(response['response'][result]['country'])
    countryList.sort()
    context = {'countryList': countryList}

    if request.method == "POST":
        selectedCountry = request.POST['selectedCountry']

        for x in range(0, noOfResults):
            if selectedCountry == response['response'][x]['country']:
                newCase = response['response'][x]['cases']['new']
                if newCase is None:
                    newCase = 0
                activeCase = response['response'][x]['cases']['active']
                if activeCase is None:
                    activeCase = 0
                criticalCases = response['response'][x]['cases']['critical']
                if criticalCases is None:
                    criticalCases = 0
                recovered = response['response'][x]['cases']['recovered']
                if recovered is None:
                    recovered = 0
                total = response['response'][x]['cases']['total']
                deaths = int(total) - int(activeCase) - int(recovered)

        context = {'selectedCountry': selectedCountry, 'countryList': countryList, 'newCases': newCase, 'activeCase': activeCase,
                   'criticalCases': criticalCases, 'recovered': recovered, 'total': total, 'deaths': deaths}
        return render(request, 'homepage.html', context)
    return render(request, 'homepage.html', context)
