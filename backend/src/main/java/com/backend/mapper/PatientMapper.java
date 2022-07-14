package com.backend.mapper;

import com.backend.pojo.Patient;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;

// 表示的这是一个mybaits的map类
@Mapper
@Repository
public interface PatientMapper {
    //根据病人id查详细数据
    Patient GetPatientsByPatientName(String patientName);
    // 新建病人
    void NewPatient(String patientName,String realname,String username,String hospital,String other);
}
