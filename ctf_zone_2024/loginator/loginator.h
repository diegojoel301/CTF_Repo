#include <string>
#include <iostream>
#include <memory>
#include <map>
#include <vector>
#include <thread>

class Loginator;

struct Note { 
  std::string note;
  bool privileged = false;
};

class User {
  public:
    User(std::string& name,std::string& password);
    virtual ~User() = default;
    std::string get_name();
    virtual void post_note(std::string& text) = 0;
    virtual std::vector<std::string> read_notes(Loginator& log,std::string& name) = 0;
    virtual void print_id(uint64_t& id) = 0;
    std::vector<Note> notes;
  private:
    std::string name;
    std::string password;
};

class Admin : public User {
  public:
    void post_note(std::string& text) override;
    std::vector<std::string> read_notes(Loginator& log,std::string& name) override;
    void print_id(uint64_t &id) override;
};

class DefaultUser : public User {
  public:
    DefaultUser(std::string& name,std::string& password) : User(name,password) {};
    ~DefaultUser() = default;
    void post_note(std::string& text) override;
    void print_id(uint64_t &id) override;
    std::vector<std::string> read_notes(Loginator& log,std::string& name) override;
};

class Loginator {
  std::map<uint64_t,std::shared_ptr<User>> users;
  std::map<uint64_t,std::shared_ptr<User>> logged_users;
  public:
    Loginator(){};
    ~Loginator() = default;
    static uint64_t make_hash(std::string& str);
    void reg(std::string& name,std::string& pass);
    int login_user(std::string& name, std::string& password);
    void logout_user(uint64_t id);
    void delete_account(uint64_t id);
    std::shared_ptr<User> find_user(uint64_t id);
    std::shared_ptr<User> find_logged_user(uint64_t id);
    void dcheck(uint64_t id);

};


