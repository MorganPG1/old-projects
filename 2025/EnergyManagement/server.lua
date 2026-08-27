---@diagnostic disable: undefined-global
--EMS SERVER BY MORGANPG
--(Energy Management System) with Data Persistence

-- Configuration
local Hostname = "main"
local METER_SAVE_FILE = "ems_meters.db"
local ACCOUNT_SAVE_FILE = "ems_accounts.db"

-- Data Tables
EnergyMeters = {}
AccountList = {}

--[[
    Example meter structure (in memory)
    {
        label="House1",
        account="morganpg",
        redstoneConfig = { relay="relay_0", side="left" }
    }

    Example account structure (in memory)
    {
        balance=1,
        energyUsed=90000,
        energyUsedSinceTopUp=0,
        energyRemaining=10000
    }
]]--

-- Function to save the current state of meters and accounts to files
local function saveData()
    -- Save EnergyMeters data
    local meterFile = fs.open(METER_SAVE_FILE, "w")
    if meterFile then
        meterFile.write(textutils.serialize(EnergyMeters))
        meterFile.close()
    else
        print("Error: Could not open meter save file for writing.")
    end

    -- Save AccountList data
    local accountFile = fs.open(ACCOUNT_SAVE_FILE, "w")
    if accountFile then
        accountFile.write(textutils.serialize(AccountList))
        accountFile.close()
    else
        print("Error: Could not open account save file for writing.")
    end
end

-- Function to load the state of meters and accounts from files
local function loadData()
    -- Load AccountList data
    if fs.exists(ACCOUNT_SAVE_FILE) then
        local accountFile = fs.open(ACCOUNT_SAVE_FILE, "r")
        if accountFile then
            local data = accountFile.readAll()
            accountFile.close()
            local success, deserialized = pcall(textutils.unserialize, data)
            if success and type(deserialized) == "table" then
                AccountList = deserialized
                print("Loaded " .. #AccountList .. " accounts.")
            else
                print("Warning: Could not load account data. File might be corrupt.")
            end
        end
    end

    -- Load EnergyMeters data into a temporary table
    local loadedMeters = {}
    if fs.exists(METER_SAVE_FILE) then
        local meterFile = fs.open(METER_SAVE_FILE, "r")
        if meterFile then
            local data = meterFile.readAll()
            meterFile.close()
            local success, deserialized = pcall(textutils.unserialize, data)
            if success and type(deserialized) == "table" then
                loadedMeters = deserialized
            else
                print("Warning: Could not load meter data. File might be corrupt.")
            end
        end
    end

    -- Scan for attached meters and populate the main EnergyMeters table
    -- This ensures we don't load data for meters that have been physically removed
    for i, name in ipairs(peripheral.getNames()) do
        if peripheral.hasType(name, "energymeter") then
            if loadedMeters[name] then
                -- If we have saved data for this meter, use it
                EnergyMeters[name] = loadedMeters[name]
            else
                -- Otherwise, initialize it as a new meter
                EnergyMeters[name] = {
                    ["label"] = "",
                    ["account"] = "",
                    ["redstoneConfig"] = {
                        ["relay"] = "",
                        ["side"] = "",
                    }
                }
            end
        end
    end
end


print("Server starting...")
loadData()

local amountOfMeters = 0
for _ in pairs(EnergyMeters) do amountOfMeters = amountOfMeters + 1 end

print("Server initialised!")
print(amountOfMeters .. " meters loaded!")

rednet.open("top")
rednet.host("EMS", Hostname)
print("Listening for requests on protocol 'EMS' with hostname '" .. Hostname .. "'...")


while true do
    local id, data, protocol = rednet.receive("EMS", 0.1)
    if id and type(data) == "table" then
        local requestFunction = data.requestFunc
        if requestFunction == "ListMeters" then
            rednet.send(id, EnergyMeters, protocol)
        elseif requestFunction == "SetLabel" then
            if EnergyMeters[data.meter] then
                EnergyMeters[data.meter].label = data.label
                rednet.send(id, "Success", protocol)
            end
        elseif requestFunction == "ConfigureMeter" then
            if EnergyMeters[data.meter] then
                EnergyMeters[data.meter].redstoneConfig = { ["relay"] = data.relay, ["side"] = data.side }
                rednet.send(id, "Success", protocol)
            end
        elseif requestFunction == "AssignAccount" then
            if EnergyMeters[data.meter] and AccountList[data.account] then
                EnergyMeters[data.meter].account = data.account
                rednet.send(id, "Success", protocol)
            else
                rednet.send(id, "Failure: Invalid meter or account", protocol)
            end
        elseif requestFunction == "ListAccounts" then
            rednet.send(id, AccountList, protocol)
        elseif requestFunction == "CreateAccount" then
            if not AccountList[data.name] then
                AccountList[data.name] = {
                    ["balance"] = 0,
                    ["energyUsed"] = 0,
                    ["energyUsedSinceTopUp"] = 0,
                    ["energyRemaining"] = 0,
                }
                rednet.send(id, "Success", protocol)
            else
                rednet.send(id, "Failure: Account already exists", protocol)
            end
        elseif requestFunction == "TopUp" then
            local account = AccountList[data.name]
            if account then
                account.energyUsedSinceTopUp = 0
                account.balance = account.balance + data.amount
                rednet.send(id, account.balance, protocol)
            end
        end
    end

    -- Process energy consumption for each meter
    for name, meter in pairs(EnergyMeters) do
        local account = AccountList[meter.account]
        local relay = peripheral.wrap(meter.redstoneConfig.relay)

        if account then
            local meterApi = peripheral.wrap(name)
            if meterApi then
                local consumption = meterApi.getTransferRate()
                local energyConsumed = consumption * (0.1 * 20) 
                
                account.energyUsedSinceTopUp = account.energyUsedSinceTopUp + energyConsumed
                account.energyUsed = account.energyUsed + energyConsumed
                account.balance = account.balance - (energyConsumed / 100000) -- 1 diamond = 100kFE
                account.energyRemaining = account.balance * 100000

                if account.balance < 0 then
                    account.balance = 0
                    account.energyRemaining = 0
                end
                 
                if relay ~= nil then
                    local hasPower = account.balance > 0
                    relay.setOutput(meter.redstoneConfig.side, not hasPower)
                end
            end
        else
            if relay ~= nil then
                relay.setOutput(meter.redstoneConfig.side, true)
            end
        end
    end

    saveData()
end
