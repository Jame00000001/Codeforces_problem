// Language: C++
// Difficulty: Easy
// Tags: Implementation, Strings

#include<iostream>
using namespace std;

int main() {
string s;
cin>> s;
int small=0,capital=0;
for(int i = 0 ; i < s.length();i++)
{
    if(s[i]>='a'&&s[i]<='z')
    {
        small++;
    }
    if(s[i]>='A'&&s[i]<='Z')
    {
        capital++;
    }
    
}
// cout<<small << " " <<captial;
if(small>=capital)
{
    for(int i = 0;i<s.length();i++)
    {
        s[i]=tolower(s[i]);
    }
    cout << s << endl;
}else{//upercae>lowercase = all letter be upercase
    for(int i = 0;i<s.length();i++)
    {
        s[i]=toupper(s[i]);
    }
    cout << s << endl;
}
}
