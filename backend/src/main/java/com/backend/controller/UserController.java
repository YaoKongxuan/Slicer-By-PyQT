package com.backend.controller;
import com.backend.mapper.PatientMapper;
import com.backend.mapper.ProjectMapper;
import com.backend.mapper.RelationshipMapper;
import com.backend.mapper.UserMapper;
import com.backend.pojo.Patient;
import com.backend.pojo.Project;
import com.esotericsoftware.yamlbeans.YamlException;
import com.esotericsoftware.yamlbeans.YamlReader;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class UserController {
    @Autowired
    UserMapper userMapper;
    @Autowired
    PatientMapper patientMapper;
    @Autowired
    ProjectMapper projectMapper;
    @Autowired
    RelationshipMapper relationshipMapper;
    // 查询用户有哪些病人和病例数据
    @RequestMapping({"/user/getdatas"})
    public Map<String, Object> GetDatas(String username)
    {
        Map<String, Object> resultMap = new HashMap<>();
        // 获取到用户拥有的项目
        List<Project> projectList = projectMapper.GetProjectsByUsername(username);
        resultMap.put("code",200);
        Map<String, Object> datas = new HashMap<>();

        resultMap.put("error",null);
        for(Project project : projectList){
            if(!datas.containsKey(project.getPatientName())){
                Patient patient = patientMapper.GetPatientsByPatientName(project.getPatientName());
                Map<String, Object> temp = new HashMap<>();
                temp.put("root",patient.getRootUser().equals(username)?"yes":"no");
                temp.put("realname",patient.getRealName());
                temp.put("patientother",patient.getOther());
                temp.put("hospital",patient.getHospital());
                Map<String, String> projectsMap = new HashMap<>();
                projectsMap.put("master","");
                temp.put("projects",projectsMap);
                datas.put(patient.getPatientName(),temp);
            }
            Map<String, Object> temppatientMap = (Map<String, Object>) datas.get(project.getPatientName());
            Map<String, String> tempprojectMap = (Map<String, String>) temppatientMap.get("projects");
            tempprojectMap.put(project.getProjectName(),project.getOther());
        }
        List<String> allprojectList = relationshipMapper.GetRelationshipsByUserName(username);
        for(String patientName:allprojectList){
            if(!datas.containsKey(patientName)){
                Patient patient = patientMapper.GetPatientsByPatientName(patientName);
                Map<String, Object> temp = new HashMap<>();
                temp.put("root",patient.getRootUser().equals(username)?"yes":"no");
                temp.put("realname",patient.getRealName());
                temp.put("patientother",patient.getOther());
                temp.put("hospital",patient.getHospital());
                Map<String, String> projectsMap = new HashMap<>();
                projectsMap.put("master","");
                temp.put("projects",projectsMap);
                datas.put(patient.getPatientName(),temp);
            }
        }
        resultMap.put("data",datas);
        return resultMap;
    }
    // 查询用户有哪些病人和病例数据
    @RequestMapping({"/user/getdowweb"})
    public Map<String, Object> GetDowWeb(String userLat,String userLon) throws FileNotFoundException, YamlException {
        Map<String, Object> resultMap = new HashMap<>();
        if (hadoopMap.isEmpty()){
            HashMap<String, String> temp01 = new HashMap<String, String>() {
                {
                    put("web", "web01");
                    put("lat", "20");
                    put("lon", "20");
                }
            };
            hadoopMap.put("hadoop01",temp01);
            HashMap<String, String> temp02 = new HashMap<String, String>() {
                {
                    put("web", "web02");
                    put("lat", "40");
                    put("lon", "40.8");
                }
            };
            hadoopMap.put("hadoop02",temp02);
            HashMap<String, String> temp03 = new HashMap<String, String>() {
                {
                    put("web", "web03");
                    put("lat", "-20");
                    put("lon", "-20");
                }
            };
            hadoopMap.put("hadoop03",temp03);
        }
        double min = Double.MAX_VALUE;
        String resWeb = "";
        for(String hadoop : hadoopMap.keySet()){
            double hadoopLat = Double.parseDouble(hadoopMap.get(hadoop).get("lat"));
            double hadoopLon = Double.parseDouble(hadoopMap.get(hadoop).get("lon"));
            double temp = GetDistance(hadoopLon,hadoopLat,Double.parseDouble(userLon),Double.parseDouble(userLat));
            if (temp<min){
                min = temp;
                resWeb = hadoopMap.get(hadoop).get("web");
            }
        }
        resultMap.put("web",resWeb);
        return resultMap;
    }
    static HashMap<String, HashMap<String, String>> hadoopMap = new HashMap<>();
    //赤道半径(单位m)
    private static double EARTH_RADIUS = 6371000;
    /**
     * 转化为弧度(rad)
     * */
    private static double rad(double d)
    {
        return d * Math.PI / 180.0;
    }
    /**
     * @param lon1 第一点的精度
     * @param lat1 第一点的纬度
     * @param lon2 第二点的精度
     * @param lat2 第二点的纬度
     * @return 返回的距离，单位m
     * */
    public static double GetDistance(double lon1,double lat1,double lon2, double lat2) {
        double radLat1 = rad(lat1);
        double radLat2 = rad(lat2);
        double a = radLat1 - radLat2;
        double b = rad(lon1) - rad(lon2);
        double s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2), 2) + Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)));
        s = s * EARTH_RADIUS;
        s = Math.round(s * 10000) / 10000;
        return s/10000;
    }
    // 删除用户-病人的项目
    @RequestMapping({"/user/delproject"})
    public Map<String, Object> DelProject(String username,String patientname,String projectname) {
        Map<String, Object> resultMap = new HashMap<>();
        projectMapper.DelProjectByUsernameAndPatientnameAndProjectname(username,patientname,projectname);
        resultMap.put("code",200);
        return resultMap;
    }

    // 新建用户-病人的项目
    @RequestMapping({"/user/newproject"})
    public Map<String, Object> NewProject(String username,String patientname,String projectname,String other) {
        Map<String, Object> resultMap = new HashMap<>();
        projectMapper.NewProjectByUsernameAndPatientnameAndProjectname(username,patientname,projectname,other);
        resultMap.put("code",200);
        return resultMap;
    }

    // 新建病人
    @RequestMapping({"/user/newpatientt"})
    public Map<String, Object> NewPatientt(String username,String patientname,String hospital,String other,String realname) {
        Map<String, Object> resultMap = new HashMap<>();
        if(patientMapper.GetPatientsByPatientName(patientname) != null) {
            resultMap.put("code", 300);
            resultMap.put("error", "病人用户名已经存在！");
        }else{
            patientMapper.NewPatient(patientname,realname,username,hospital,other);
            relationshipMapper.NewRelationship(username,patientname);
            resultMap.put("code",200);
            resultMap.put("error", null);
        }
        return resultMap;
    }

    // 添加权限
    @RequestMapping({"/user/addrelationship"})
    public Map<String, Object> AddRelationship(String username,String patientname) {
        Map<String, Object> resultMap = new HashMap<>();
        if(userMapper.SearchUserByUsername(username) == null) {
            resultMap.put("code", 300);
            resultMap.put("error", "要添加的用户不存在！");
        }else{
            if(relationshipMapper.GetRelationship(username,patientname) != null){
                resultMap.put("code", 300);
                resultMap.put("error", "添加的用户已经拥有该病人的权限！");
            } else {
                relationshipMapper.NewRelationship(username,patientname);
                resultMap.put("code",200);
                resultMap.put("error", null);
            }
        }
        return resultMap;
    }
}