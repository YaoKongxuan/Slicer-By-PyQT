package com.backend.config;

import com.backend.mapper.UserMapper;
import org.apache.shiro.authc.*;
import org.apache.shiro.authz.AuthorizationInfo;
import org.apache.shiro.realm.AuthorizingRealm;
import org.apache.shiro.subject.PrincipalCollection;
import org.springframework.beans.factory.annotation.Autowired;

public class UserRealm extends AuthorizingRealm {

    @Autowired
    UserMapper userMapper;
    //授权
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principalCollection) {
        return null;
    }
    //认证
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken authenticationToken) throws AuthenticationException {
        //用户密码从数据库中取
        UsernamePasswordToken userToken = (UsernamePasswordToken) authenticationToken;
        String psw = userMapper.SearchUserPassword(userToken.getUsername());
        if(psw == null)
        {
            // 用户名认证
            // 返回null抛出用户名不存在异常
            return null;
        }
        return new SimpleAuthenticationInfo(userToken.getUsername(),psw,"");
    }
}
