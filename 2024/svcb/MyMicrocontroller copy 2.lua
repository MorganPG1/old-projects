--- Developed using LifeBoatAPI - Stormworks Lua plugin for VSCode - https://code.visualstudio.com/download (search "Stormworks Lua with LifeboatAPI" extension)
--- If you have any issues, please report them here: https://github.com/nameouschangey/STORMWORKS_VSCodeExtension/issues - by Nameous Changey


--[====[ HOTKEYS ]====]
-- Press F6 to simulate this file
-- Press F7 to build the project, copy the output from /_build/out/ into the game to use
-- Remember to set your Author name etc. in the settings: CTRL+COMMA


--[====[ EDITABLE SIMULATOR CONFIG - *automatically removed from the F7 build output ]====]
---@section __LB_SIMULATOR_ONLY__
do
    ---@type Simulator -- Set properties and screen sizes here - will run once when the script is loaded
    simulator = simulator
    simulator:setScreen(1, "3x3")
    simulator:setProperty("ExampleNumberProperty", 123)

    -- Runs every tick just before onTick; allows you to simulate the inputs changing
    ---@param simulator Simulator Use simulator:<function>() to set inputs etc.
    ---@param ticks     number Number of ticks since simulator started
    function onLBSimulatorTick(simulator, ticks)

        -- touchscreen defaults
        local screenConnection = simulator:getTouchScreen(1)
        simulator:setInputBool(1, screenConnection.isTouched)
        simulator:setInputNumber(1, screenConnection.width)
        simulator:setInputNumber(2, screenConnection.height)
        simulator:setInputNumber(3, screenConnection.touchX)
        simulator:setInputNumber(4, screenConnection.touchY)
        simulator:setInputNumber(5, 1)
        simulator:setInputNumber(6, 2)
        simulator:setInputNumber(7, 0)
        simulator:setInputNumber(8, 1123431234)
        simulator:setInputBool(2, true)
        simulator:setInputBool(3, true)
        simulator:setInputBool(4, true)
        -- NEW! button/slider options from the UI
        simulator:setInputBool(31, simulator:getIsToggled(1))       -- if button 1 is clicked, provide an ON pulse for input.getBool(31)
        simulator:setInputNumber(31, simulator:getSlider(1))        -- set input 31 to the value of slider 1

        simulator:setInputBool(32, simulator:getIsToggled(2))       -- make button 2 a toggle, for input.getBool(32)
        simulator:setInputNumber(32, simulator:getSlider(2) * 50)   -- set input 32 to the value from slider 2 * 50
    end;
end
---@endsection


--[====[ IN-GAME CODE ]====]

-- try require("Folder.Filename") to include code from another file in this, so you can store code in libraries
-- the "LifeBoatAPI" is included by default in /_build/libs/ - you can use require("LifeBoatAPI") to get this, and use all the LifeBoatAPI.<functions>!

ticks = 0
timer = 0
moduleId = 2
faults = {}
waitingForResponse = false
function splitString(inputstr, n)
    local t = {}
    for m in inputstr:gmatch(('.'):rep(n)) do
        table.insert(t, m)
    end
    return t
end

function isInTable(value, table)
    for index, val in ipairs(table) do
        if val == value then
            return index
        end
    end
    return false
end
function SendCommand(id, command, data)
    output.setNumber(5, id)
    output.setNumber(6, moduleId)
    output.setNumber(7, command)
    output.setNumber(8, data)
    waitingForResponse = true
end

function AwaitResponse()
    if input.getBool(3) and input.getNumber(5) == moduleId then
        return input.getNumber(8)
    else
        return nil
    end
end

function GetCommand()
    if not input.getBool(3) then
        if input.getNumber(5) == -1 or input.getNumber(5) == moduleId then
            return true, input.getBool(6), input.getBool(7), input.getBool(8)
        else
            return false, nil, nil, nil
            
        end

    else
        return false, nil, nil, nil
    end
end

function AddFault(fault)
    table.insert(faults, fault)
end

function RemoveFault(fault)
    index = isInTable(fault, faults)
    if index then
        table.remove(faults, index)
    end
end

function GetFaults()
    stringval = ""
    for index, value in ipairs(faults) do
        --print(index, value)
        stringval = stringval..tostring(value)
        --print(stringval)
    end

    if stringval ~= "" then
        return tonumber(stringval)
    else
        --print(stringval)
        return 0
    end
end
function DecodeFaults(faultsVal)
    if faultsVal ~= 0 then
        local faultStr = tostring(faultsVal)
        if string.len(faultStr) % 5 then
            local faultsList = splitString(faultStr, 5)
            for index, value in ipairs(faultsList) do
                local faultSevere = string.sub(value, 1, 1)
                local faultData = string.sub(value, 2)
                if faultSevere == "3" then
                    faultSevere = "D"
                elseif faultSevere == "2" then
                    faultSevere = "C"
                elseif faultSevere == "1" then
                    faultSevere = "B"
                elseif faultSevere == "0" then
                    faultSevere = "A"
                end
                faultsList[index] = faultSevere..faultData
            end
            return faultsList
        else
            return false
        end
    else
        return false
    end
end
function onTick()
    ticks = ticks + 1
    timer = timer + 1
    --[[
    local faultString = GetFaults()
    local faultsLst = DecodeFaults(faultString)
    if faultsLst then
        for index, value in ipairs(faultsLst) do
            print(value)
        end
    end
    ]]--

    if waitingForResponse then
        local response = AwaitResponse()
        if response then
            local decoded = DecodeFaults(response)
            if decoded then
                for index, value in ipairs(decoded) do
                    --print(value)
                end
            end
            waitingForResponse = false
        end
    else
        local  iscommand, sender, command, data = GetCommand()
        if iscommand then
            --Handle commands here
            
        else
            local recv = input.getNumber(5)
            local sendr = input.getNumber(6)
            local cmd = input.getNumber(7)
            local data = input.getNumber(8)
            local busWrk = input.getBool(2)
            local rsp = input.getBool(3)
            local rdy = input.getBool(4)

            output.setNumber(5, recv)
            output.setNumber(6, sendr)
            output.setNumber(7, cmd)
            output.setNumber(8, data)
            output.setBool(2, busWrk)
            output.setBool(3, rsp)
            output.setBool(4, rdy)

            
        end
    end

    if ticks >= 120 and ticks <= 125 then
        SendCommand(-1, 5, 1221)
    end
end

function onDraw()
    screen.drawCircle(16,16,5)
end



