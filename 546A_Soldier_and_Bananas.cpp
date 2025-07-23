// Language: C++
// Difficulty: Easy
// Tags: Math, Implementation, Brute Force

#include<iostream>
using namespace std;

int main() {
    int k,n,w,total_amount=0;
    cin>>k>>n>>w;
    total_amount = (k*(w*(w+1))/2);

    int borrow = total_amount-n;
    if(borrow<0)
       borrow=0;
    cout << borrow<<endl;
   
    return 0;
}
