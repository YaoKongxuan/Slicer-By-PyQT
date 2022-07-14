package com.backend.controller;

import com.backend.mapper.UserMapper;
import org.apache.shiro.SecurityUtils;
import org.apache.shiro.authc.IncorrectCredentialsException;
import org.apache.shiro.authc.UnknownAccountException;
import org.apache.shiro.authc.UsernamePasswordToken;
import org.apache.shiro.subject.Subject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class Login {
    @Autowired
    UserMapper userMapper;

    /**
     * 登陆功能
     * @param username 用户id
     * @param password 用户密码
     * @return 是否登陆成功
     */
    @RequestMapping({"/login/tologin"})
    public Map<String, Object> tologin(String username, String password)
    {
        Map<String, Object> resultMap = new HashMap<>();
        //获取当前用户
        Subject subject = SecurityUtils.getSubject();
        //封装用户的登录信息
        UsernamePasswordToken token = new UsernamePasswordToken(username,password);
        //执行登录操作
        try{
            subject.login(token);
            resultMap.put("code",200);
            resultMap.put("user",userMapper.SearchUserByUsername(username));
            resultMap.put("error",null);
        }
        catch (UnknownAccountException e)//用户名不存在
        {
            resultMap.put("code",404);
            resultMap.put("user",null);
            resultMap.put("error","用户名不存在");
            return resultMap;
        }
        catch (IncorrectCredentialsException e)//密码错误
        {
            resultMap.put("code",300);
            resultMap.put("user",null);
            resultMap.put("error","密码错误");
            return resultMap;
        }
        return resultMap;
    }

    /**
     * 注册功能
     * @param username 用户名
     * @param password 用户密码
     * @param realName 真实姓名
     * @param hospital 所在医院
     * @return 是否注册成功
     */
    @RequestMapping({"/login/zhuce"})
    public Map<String, Object> zhuce(String username, String password,String realName, String hospital)
    {
        Map<String, Object> resultMap = new HashMap<>();
        try{
            if(userMapper.SearchUserPassword(username) == null){
                userMapper.NewUser(username,password,realName,hospital);
                resultMap.put("code",200);
                resultMap.put("user",null);
                resultMap.put("error",null);
                return resultMap;
            } else {
                resultMap.put("code",300);
                resultMap.put("user",null);
                resultMap.put("error","用户名重复,请输入其他用户名");
                return resultMap;
            }
        }
        catch (Error ignored){
            resultMap.put("code",500);
            resultMap.put("user",null);
            resultMap.put("error","注册用户失败,请重试");
            return resultMap;
        }
    }
}
