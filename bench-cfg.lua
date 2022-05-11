#!/usr/bin/env ../src/tarantool

os.execute('rm -rf *.snap *.xlog *.vylog ./512 ./513 ./514 ./515 ./516 ./517 ./518 ./519 ./520 ./521')

local engine = arg[1]
local wal_mode = arg[2]

if #arg < 1 then
    engine = 'memtx'
end

if #arg < 2 then
    wal_mode = 'none'
end

--require('fiber').set_default_slice(1000000)

box.cfg {
    slab_alloc_arena    = 1,
    pid_file            = "tarantool.pid",
    wal_mode            = wal_mode,
    snap_dir = ".",
    work_dir = "."
}

-- Tests to run
tests = {'replaces', 'selects', 'selrepl', 'updates', 'deletes'}
-- Workloads
workloads = {
    -- Run one extra test to warm up the server
    {tests = tests, type = 'hash', parts = { 'num' }},
    {tests = tests, type = 'hash', parts = { 'num' }},
--    {tests = tests, type = 'hash', parts = { 'str' }},
    {tests = tests, type = 'tree', parts = { 'num' }},
  --  {tests = tests, type = 'tree', parts = { 'str' }},
--[[
    {tests = tests, type = 'hash', parts = { 'num', 'num' }},
    {tests = tests, type = 'hash', parts = { 'num', 'str'}},
    {tests = tests, type = 'hash', parts = { 'str', 'num' }},
    {tests = tests, type = 'hash', parts = { 'str', 'str' }},
    {tests = tests, type = 'tree', parts = { 'num' }},
    {tests = tests, type = 'tree', parts = { 'str' }},
    {tests = tests, type = 'tree', parts = { 'num', 'num' }},
    {tests = tests, type = 'tree', parts = { 'num', 'str' }},
    {tests = tests, type = 'tree', parts = { 'str', 'num' }},
    {tests = tests, type = 'tree', parts = { 'str', 'str' }}
--]]
}

local bench = require('cbench')
local json = require('json')

print('Benchmarking...')
-- Run benchmark
result = bench.run(workloads, 1000000, 5, engine);
print('Done')

-- Encode the result and save to a file
json_result = json.encode(result)
filename = string.format('bench-result-%s.json',
    box.info.version);
file = io.open(filename, 'w')
file:write(json_result)
file:flush()
file:close()
print('Benchmark result saved to ', filename)

os.exit(0)
