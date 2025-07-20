#include<iostream>
using namespace std;
//#define long long;

int main() {
    long long m,n,a,number;
    cin >> m >> n >> a;
    number = (n/a+(n%a!=0))*(m/a+(m%a!=0));
    cout << number;
    return 0;
}