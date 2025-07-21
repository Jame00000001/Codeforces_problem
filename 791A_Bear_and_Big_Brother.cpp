#include<iostream>
using namespace std;

int main() {
    int a,b,year=0;
    cin >> a>> b;
 
    while(a<=b)
    {
        a*=3;
        a*=2;
    }
    
 
    cout << year << endl;

    return 0;
}