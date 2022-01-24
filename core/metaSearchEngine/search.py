from serpapi import GoogleSearch
from serpapi import BaiduSearch
import math
import numpy as np


def google_result(query):
        params = {
          "engine": "google",
          "q": query,
          "api_key": "53204d8dde202e10b0c7e55d5239659c113d52e7750359f3caebaaf2ba771f03"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results['organic_results']

        return organic_results

def baidu_result(query):
    params = {
      "engine": "baidu",
      "q": query,
      "api_key": "53204d8dde202e10b0c7e55d5239659c113d52e7750359f3caebaaf2ba771f03"
    }

    search = BaiduSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']
    return organic_results

def bing_result(query):

    params = {
      "engine": "bing",
      "q": query,
      "api_key": "53204d8dde202e10b0c7e55d5239659c113d52e7750359f3caebaaf2ba771f03"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']
    return organic_results

def ddg_result(query):

    params = {
      "engine": "duckduckgo",
      "q": query,
      "api_key": "53204d8dde202e10b0c7e55d5239659c113d52e7750359f3caebaaf2ba771f03"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']

    return organic_results

def yahoo_result(query):

    params = {
      "engine": "yahoo",
      "p": query,
      "api_key": "53204d8dde202e10b0c7e55d5239659c113d52e7750359f3caebaaf2ba771f03"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results['organic_results']
    return organic_results

def buildTransition(inputLists, space):
    nList = len(inputLists)
    
    topK = space[:]
    
    for i in range(nList):
        n = len(inputLists[i])
        topKList = [n]*len(space[i])
        indices = []
        for j in range(len(inputLists[i])):
            indices.append(space[i].index(inputLists[i][j]))
        
        j = 0
        for idx in indices:
            topKList[idx] = j
            j+=1
        
        topK[i] = topKList
        
    L = list(set([x for l in inputLists for x in l]))
    N = len(L)
    
    MC1 = np.zeros((N,N))
    MC2 = np.zeros((N,N))
    MC3 = np.zeros((N,N))
    
    lookup = []
    for l1 in L:
        for l2 in L:
            if l1!=l2:
                temp = [l1, l2]
                lookup.append(temp)
    
    for i in range(len(lookup)):
        a = lookup[i][0]
        b = lookup[i][1]
        found = 0
        nn = 0
        for j in range(nList):
            found += (a in space[j])*(b in space[j])
            nn += (topK[j][space[j].index(a)]>
                        topK[j][space[j].index(b)])
            
        index1 = L.index(a)
        index2 = L.index(b)
        
        MC1[index1, index2] = math.ceil(float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        MC2[index1, index2] = math.floor(float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        MC3[index1, index2] = (float(nn)/(found*(found!=0)+(found+1)*(found==0)))+0.5*(found==0)
        
    MC1=MC1/float(N)
    MC2=MC2/float(N)
    MC3=MC3/float(N)
     

    for i in range(N):
        MC1[i,i]=1-sum(MC1[i])
        MC2[i,i]=1-sum(MC2[i])
        MC3[i,i]=1-sum(MC3[i])
  
    return L, MC1, MC2, MC3

def MC_ranks(elements, trans, a = 0.15, delta = 0.011):
        n=trans.shape[0] # number of rows
        trans= trans * float((1-a)) # multiply and add all elements
        trans= trans + float(a)/float(n)
        A= np.zeros((n,n))
        for x in range(n):
                A[x,x]=1

        difference= 1
        count=0
        while difference>delta:
                A1= np.matmul(A,trans)
                temp= A1-A
                difference= float(temp.max())
                A= A1
                count+=1


        # Aaauming A1 in a 1 x n matrix
        #Assuming Elements= [a,b,c,d]
        
        A1= A1[0,:] #get first row of the matrix
        temp=A1.tolist() # temp should have this structure [n1, n2, n3]
        ranked_ele=[]
        for i in range(n):
                max_ele=max(temp)
                index= temp.index(max_ele)
                element=elements[index]
                ranked_ele.append(element)
                temp[index]=-1

        A1= -np.sort(-A1)
        results=[]
        results.append(count)
        results.append(A1)
        results.append(ranked_ele)

        return results

def MC(inputLists, k=0, a=0.15, delta=10^-15):    
    space = list(set([x for l in inputLists for x in l]))
    space.sort();
    space = [space]*len(inputLists)
    
    
    L, MC1, MC2, MC3 = buildTransition(inputLists, space)
    
    N =len(L)
    if k ==0:
        k = N
    
    MC1Ranks = MC_ranks(L, MC1)
    MC2Ranks = MC_ranks(L, MC2)
    MC3Ranks = MC_ranks(L, MC3)

#    print MC1
#    print MC2
#    print MC3  

    # print(MC1Ranks[2], MC1Ranks[1])
    # print(MC2Ranks[2], MC2Ranks[1])
    # print(MC3Ranks[2], MC3Ranks[1])
    
    print("\n\n************* RESULT *********************")
    top=0
    final=[]
    for ele in MC3Ranks[2]:
        print(ele)
        final.append(ele)
        top+=1
        if(top==10):
            break

    return final

def search_result(query):
    g_result = google_result(query)
    bing_Result = bing_result(query)
    baidu_Result = baidu_result(query)
    duckduckgo_result = ddg_result(query)
    yahoo_Result = yahoo_result(query)

    results = []

    results.append([item['link'] for item in g_result])
    results.append([item['link'] for item in bing_Result])
    results.append([item['link'] for item in baidu_Result])
    results.append([item['link'] for item in duckduckgo_result])
    results.append([item['link'] for item in yahoo_Result])

    final_result = MC(results)

    title_result = []

    for i in final_result:
        if i in results[0]:
            title_result.append(g_result[results[0].index(i)]['title'])

        elif i in results[1]:
            title_result.append(bing_Result[results[1].index(i)]['title'])

        elif i in results[2]:
            title_result.append(baidu_Result[results[2].index(i)]['title'])

        elif i in results[3]:
            print(results[3].index(i))
            title_result.append(duckduckgo_result[results[3].index(i)]['title'])

        elif i in results[4]:
            title_result.append(yahoo_Result[results[4].index(i)]['title'])

    return (title_result, final_result)

def main():
    query = input('please input your query:')

    g_result = google_result(query)
    bing_Result = bing_result(query)
    baidu_Result = baidu_result(query)
    duckduckgo_result = ddg_result(query)
    yahoo_Result = yahoo_result(query)

    results = []

    results.append([item['link'] for item in g_result])
    results.append([item['link'] for item in bing_Result])
    results.append([item['link'] for item in baidu_Result])
    results.append([item['link'] for item in duckduckgo_result])
    results.append([item['link'] for item in yahoo_Result])

    final_result = MC(results)

if __name__ == '__main__':
    main()