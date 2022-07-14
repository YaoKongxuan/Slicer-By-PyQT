package com.backend.mapper;

import com.backend.pojo.User;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

//表示的这是一个mybaits的map类
@Mapper
@Repository
public interface UserMapper {
    // 查询用户密码
    String SearchUserPassword(String username);
    // 查询全部用户
    List<User> SearchAllUser();
    // 新建用户
    Void NewUser(String username,String pwd,String realName,String hospital);
    // 根据用户名查询信息
    User SearchUserByUsername(String username);
}
