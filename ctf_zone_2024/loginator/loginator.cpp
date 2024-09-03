#include "loginator.h"

std::string User::get_name() {
  return name;
}

User::User(std::string& name, std::string& password) {
  this->name = name;
  this->password = password;
}

void Admin::post_note(std::string& text) {
  Note nt;
  nt.privileged = true;
  std::cout<<text.size()<<"\n";
  nt.note.reserve(text.size());
  nt.note = text;
  this->notes.push_back(nt);
}

std::vector<std::string> Admin::read_notes(Loginator& log,std::string& name) {
  uint64_t id = Loginator::make_hash(name);
  std::vector<std::string> notex;
  std::shared_ptr<User> usr = log.find_user(id);
  if(usr!=nullptr){

    for(auto i:usr->notes)
      notex.push_back(i.note);
  }

  return notex;
}

void Admin::print_id(uint64_t &id) {
  std::cout<<"Admin id is: "<<id<<"\n";
}

void DefaultUser::post_note(std::string& text) {
  Note nt;
  nt.privileged = false;
  std::cout<<text.size()<<"\n";
  nt.note.reserve(text.size());
  nt.note = text;
  this->notes.push_back(nt);
}

void DefaultUser::print_id(uint64_t &id) {
  std::cout<<"User id is: "<<id<<"\n";
}

std::vector<std::string> DefaultUser::read_notes(Loginator& log,std::string& name) {
  std::vector<std::string> notes;
  uint64_t id = Loginator::make_hash(name);
  std::shared_ptr<User> usr = log.find_user(id);
  if (usr != nullptr) {
    for(auto i : usr->notes) {
      if(!i.privileged)
        notes.push_back(i.note);
    }
  }
  return notes;
}

uint64_t Loginator::make_hash(std::string& name) {
  uint64_t hash = 0;

  for(auto i:name)
    hash+=i;

  return hash;
}

void Loginator::reg(std::string& name,std::string& password) {
  std::shared_ptr<DefaultUser> user = std::make_shared<DefaultUser>(name,password);
  uint64_t hash = Loginator::make_hash(name);
  users[hash] = user;
}

int Loginator::login_user(std::string& name,std::string& password) {
  uint64_t hash = Loginator::make_hash(name);
  if(logged_users.find(hash) != logged_users.end())
    return 0;
  std::shared_ptr<User> user = std::shared_ptr<User>(find_user(hash).get());
  if(user == nullptr)
    return -1;
  logged_users[hash] = user;
  return 0;
}

void Loginator::delete_account(uint64_t id) {
  users.erase(id);
};

void Loginator::logout_user(uint64_t id) {

};

std::shared_ptr<User> Loginator::find_user(uint64_t id) {
  auto res = this->users.find(id);
  if(res == users.end())
    return nullptr;
  return (*res).second;
}

std::shared_ptr<User> Loginator::find_logged_user(uint64_t id) {
  auto res = this->logged_users.find(id);
  if(res == logged_users.end())
    return nullptr;
  return (*res).second;
}

void Loginator::dcheck(uint64_t id){
  if(users[id].get() == logged_users[id].get())
    std::cout<<"Eq\n";
  else 
    std::cout<<"Not eq\n";
  if(users[id] == logged_users[id])
    std::cout<<"sm ptr eq\n";
  else
    std::cout<<"sm ptrs not eq\n";
  std::cout<<users[id].use_count()<<"\n";
  std::cout<<logged_users[id].use_count()<<"\n";
  return;
}


