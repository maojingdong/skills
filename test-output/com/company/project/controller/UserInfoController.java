package com.company.project.controller;

import com.company.project.entity.UserInfo;
import com.company.project.service.UserInfoService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * UserInfo控制器
 */
@RestController
@RequestMapping("/api/userInfo")
@Api(tags = "UserInfo管理")
public class UserInfoController {

    @Autowired
    private UserInfoService userInfoService;

    @PostMapping
    @ApiOperation("创建UserInfo")
    public UserInfo create(@RequestBody UserInfo userInfo) {
        userInfoService.save(userInfo);
        return userInfo;
    }

    @GetMapping("/{id}")
    @ApiOperation("根据ID获取UserInfo")
    public UserInfo getById(
            @ApiParam("UserInfoID") @PathVariable Long id) {
        return userInfoService.getById(id);
    }

    @GetMapping
    @ApiOperation("分页查询UserInfo列表")
    public Page<UserInfo> getPage(
            @ApiParam("页码") @RequestParam(defaultValue = "1") Integer current,
            @ApiParam("每页大小") @RequestParam(defaultValue = "10") Integer size) {
        Page<UserInfo> page = new Page<>(current, size);
        return userInfoService.page(page);
    }

    @PutMapping("/{id}")
    @ApiOperation("更新UserInfo")
    public boolean update(
            @ApiParam("UserInfoID") @PathVariable Long id,
            @RequestBody UserInfo userInfo) {
        userInfo.setUserId(id);
        return userInfoService.updateById(userInfo);
    }

    @DeleteMapping("/{id}")
    @ApiOperation("删除UserInfo")
    public boolean delete(
            @ApiParam("UserInfoID") @PathVariable Long id) {
        return userInfoService.removeById(id);
    }

    @GetMapping("/list")
    @ApiOperation("查询所有UserInfo")
    public List<UserInfo> listAll() {
        return userInfoService.list();
    }
}