package com.company.project.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.io.Serializable;
import java.time.LocalDateTime;


/**
 * UserInfo实体类

 * 用户信息表

 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ApiModel(value = "UserInfo对象", description = "UserInfo实体类")
@TableName("t_user_info")
public class UserInfo implements Serializable {

    private static final long serialVersionUID = 1L;
    

    
    @ApiModelProperty(value = "用户ID")
    @TableId(value = "user_id", type = IdType.AUTO)
    private Long userId;
    

    
    @ApiModelProperty(value = "用户名", required = true)
    @TableField("user_name")
    private String userName;
    

    
    @ApiModelProperty(value = "邮箱地址")
    @TableField("user_email")
    private String userEmail;
    

    
    @ApiModelProperty(value = "手机号码")
    @TableField("phone_number")
    private String phoneNumber;
    

    
    @ApiModelProperty(value = "用户状态：1-正常，0-禁用")
    @TableField("user_status")
    private Integer userStatus;
    

    
    @ApiModelProperty(value = "创建时间")
    @TableField("create_time")
    private LocalDateTime createTime;
    

    
    @ApiModelProperty(value = "更新时间")
    @TableField("update_time")
    private LocalDateTime updateTime;
    


}