package com.backend.mapper;

import com.backend.pojo.Project;
import com.backend.pojo.User;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

//表示的这是一个mybaits的map类
@Mapper
@Repository
public interface ProjectMapper {
    //根据username获取自己能下载的全部数据
    List<Project> GetProjectsByUsername(String username);
    void DelProjectByUsernameAndPatientnameAndProjectname(String username,String patientname,String projectname);
    void NewProjectByUsernameAndPatientnameAndProjectname(String username,String patientname,String projectname,String other);
}
