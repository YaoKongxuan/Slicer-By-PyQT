package com.backend.controller;
import com.backend.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
/*
@RestController
public class RootController {
    @Autowired
    UserMapper userMapper;
    @Autowired
    MachineMapper machineMapper;
    //查询用户信息
    @RequestMapping({"/root/searchall"})
    String SearchAllUser(Model model)
    {
        model.addAttribute("msg",userMapper.SearchAllUser());
        return "/root/searchalluser";
    }
    //查询单个用户全部信息
    @RequestMapping({"/root/searuser"})
    String SearchUser(String username,Model model)
    {
        model.addAttribute("msg",machineMapper.SearchMachineByUsername(username));
        return "/root/searchuser";
    }
    //返回root用户主页
    @RequestMapping({"/root/zhuye"})
    String Index()
    {
        return "/root/zhuye";
    }
}
*/