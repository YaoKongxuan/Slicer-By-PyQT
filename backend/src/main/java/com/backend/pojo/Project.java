package com.backend.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * patientName 病人独特名称
 * doctorName 医生独特user名称
 * other 病例其他信息
 * root 医生对这个病例是否是管理员权限，默认第一个创建病例的就是管理员
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Project {
    private String patientName;
    private String userName;
    private String projectName;
    private String other;
}
