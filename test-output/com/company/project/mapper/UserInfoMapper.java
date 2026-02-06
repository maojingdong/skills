package com.company.project.mapper;

import com.company.project.entity.UserInfo;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * UserInfoMapper接口
 */
@Mapper
public interface UserInfoMapper extends BaseMapper<UserInfo> {

    // 可在此处添加自定义查询方法
    
}