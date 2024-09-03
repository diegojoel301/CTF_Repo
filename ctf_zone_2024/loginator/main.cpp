#include <string>
#include <iostream>
#include <memory>
#include <map>
#include <vector>
#include <thread>
#include "loginator.h"


void user_menu();

void post_wrapper(std::shared_ptr<User> usr,std::string& text) {
  usr->post_note(text);
}

void read_wrapper(std::shared_ptr<User> usr,Loginator& log,std::string& name) {
  std::vector<std::string> notes = usr->read_notes(log,name);
  for(auto i : notes)
    std::cout<<i<<"\n";
}

void delete_acc_wrapper(Loginator& log,std::string& name) {
  log.delete_account(Loginator::make_hash(name));
}

void user_func(Loginator& log,std::shared_ptr<User> usr) {
  int option = 0;
  std::string name;
  std::string text;
  while(true) {
    user_menu();
    std::cin>>option;
    switch(option) {
      case 0:
      { 
        std::string usrname = usr->get_name();
        uint64_t id  =Loginator::make_hash(usrname); 
          usr->print_id(id);
      }
      break;
      case 1:
      {
        std::cout<<"Enter notes to post: \n";
        std::cin>>text;
        usr->post_note(text);
      }
      break;
      case 2:
      {
        std::cout<<"Enter user name to read: \n";
        std::cin>>name;
        usr->read_notes(log,name);
      }
      break;
      case 3:
      { 
        std::string namex = usr->get_name();
        log.logout_user(Loginator::make_hash(namex));
        return;
      }
      break;
      case 4:
      {
        std::string namex = usr->get_name();
        log.delete_account(Loginator::make_hash(namex));
      }
      break;
    }
  }

}

void main_menu() {
  std::cout<<"Enter 1 to register user.\n";
  std::cout<<"Enter 2 to login user.\n";
  std::cout<<"Enter 3 to exit.\n";
  std::cout<<">>\n";
}

void user_menu() { 
  std::cout<<"Enter 0 to print id.\n";
  std::cout<<"Enter 1 to post note.\n";
  std::cout<<"Enter 2 to read user note.\n";
  std::cout<<"Enter 3 to logout.\n";
  std::cout<<"Enter 4 to delete_account.\n";
  std::cout<<">>\n";
}

int main() {
  Loginator log;
  int option;
  while(true) {
    main_menu();
    std::cin>>option;
    switch(option) {
      case 1:
      {
        std::string name;
        std::string password;
        std::cout<<"Enter name: \n";
        std::cin>>name;
        std::cout<<"Enter pass: \n";
        std::cin>>password;
        log.reg(name,password);
      }
      break;
      case 2:
      {
        std::string name;
        std::string password;
        std::cout<<"Enter name: \n";
        std::cin>>name;
        std::cout<<"Enter pass: \n";
        std::cin>>password;
        int res = log.login_user(name,password);
        if (res!=-1)
          user_func(log,log.find_logged_user(Loginator::make_hash(name)));
        else
          std::cout<<"Invalid creds\n";
      }
      break;
      case 3:
        return 0;
      break;

    }
  }
  return 0;
}
