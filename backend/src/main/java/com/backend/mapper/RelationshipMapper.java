package com.backend.mapper;

import com.backend.pojo.Patient;
import com.backend.pojo.Relationship;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

// 表示的这是一个mybaits的map类
@Mapper
@Repository
public interface RelationshipMapper {
    //根据用户id查详细数据
    List<String> GetRelationshipsByUserName(String username);
    //新建关系
    void NewRelationship(String username,String patientname);

    //查询是否有关系
    Relationship GetRelationship(String username,String patientname);
}
