#include <iostream>
#include <functional>

void save_with_free_fun(const std::string& file_name)
{
    std::cout << "free function: " << file_name << std::endl;
}

class FileSave
{
private:

public:
    FileSave() = default;
    ~FileSave() = default;

    void save_with_member_fun(const std::string& file_name)
    {
        std::cout << "member function: " << file_name << std::endl;
    }
};

int main()
{
    FileSave file_save;

    auto save_with_lambda_fun = [](const std::string &file_name) -> void
    {
        std::cout << "lambda function: " << file_name << std::endl;
    };

    // save_with_free_fun("file.txt");
    // file_save.save_with_member_fun("file.txt");
    // save_with_lambda_fun("file.txt");

    std::function<void(const std::string&)> save1 = save_with_free_fun;
    std::function<void(const std::string&)> save2 = save_with_lambda_fun;
    std::function<void(const std::string&)> save3 = std::bind(&FileSave::save_with_member_fun, &file_save, std::placeholders::_1);

    save1("file.txt");
    save2("file.txt");
    save3("file.txt");

    return 0;
}
