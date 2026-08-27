-- EMS CLIENT BY MORGANPG
-- (Energy Management System) - v2

-- Configuration
local serverHostname = "main"
local serverProtocol = "EMS"

-- Function to clear the screen and print a header
local function printHeader(title)
    term.clear()
    term.setCursorPos(1, 1)
    print("========================================")
    print("        Energy Management System        ")
    print("========================================")
    term.setCursorPos(1, 5)
    if title then
        print("--- " .. title .. " ---")
    end
end

-- Function to send a request to the server and get a response
local function serverRequest(data)
    -- Ensure we have a connection before sending
    local serverId = rednet.lookup(serverProtocol, serverHostname)
    if not serverId then
        print("Error: Lost connection to server.")
        sleep(2)
        return nil
    end

    rednet.send(serverId, data, serverProtocol)
    local id, response = rednet.receive(serverProtocol, 5)
    if not id then
        print("Error: No response from server.")
        sleep(2)
        return nil
    end
    return response
end

-- Function to display a menu and get user input
local function showMenu(options)
    for i, option in ipairs(options) do
        print(i .. ". " .. option)
    end
    write("> ")
    local choice = read()
    return tonumber(choice)
end

-- Forward declarations to resolve function call order issues
-- This tells Lua that these functions exist, even though they are defined later.
local manageMeter
local viewAccount

-- Meter Management Functions
local function listMeters()
    while true do
        printHeader("List Meters")
        local meters = serverRequest({ requestFunc = "ListMeters" })
        if not meters then return end -- Exit if server connection lost

        local meterNames = {}
        for name, _ in pairs(meters) do
            table.insert(meterNames, name)
        end
        table.sort(meterNames)

        if #meterNames == 0 then
            print("No meters found.")
            sleep(2)
            return
        end

        printHeader("Select a Meter")
        for i, name in ipairs(meterNames) do
            local meterInfo = meters[name] or {}
            local label = meterInfo.label and meterInfo.label ~= "" and meterInfo.label or "No Label"
            local account = meterInfo.account and meterInfo.account ~= "" and meterInfo.account or "Unassigned"
            print(i .. ". " .. name .. " (" .. label .. " | " .. account .. ")")
        end
        print((#meterNames + 1) .. ". Back")

        write("> ")
        local choice = tonumber(read())
        
        if choice == #meterNames + 1 or choice == nil then
            break
        elseif choice > 0 and choice <= #meterNames then
            -- Call the manageMeter function which is now forward-declared
            manageMeter(meterNames[choice], meters)
        end
    end
end

manageMeter = function(meterName, allMeters)
    -- We get allMeters so we can refresh the specific meter's data without a new request
    local meterData = allMeters[meterName]

    while true do
        printHeader("Manage Meter: " .. meterName)
        print("Label: " .. (meterData.label and meterData.label ~= "" and meterData.label or "N/A"))
        print("Assigned Account: " .. (meterData.account and meterData.account ~= "" and meterData.account or "N/A"))
        print("Relay: " .. (meterData.redstoneConfig.relay and meterData.redstoneConfig.relay ~= "" and meterData.redstoneConfig.relay or "N/A"))
        print("Side: " .. (meterData.redstoneConfig.side and meterData.redstoneConfig.side ~= "" and meterData.redstoneConfig.side or "N/A"))
        print("----------------------------------------")
        print("1. Set Label")
        print("2. Configure Redstone Relay")
        print("3. Assign Account")
        print("4. Back")

        local choice = showMenu({})

        if choice == 1 then
            print("Enter new label:")
            local newLabel = read()
            local response = serverRequest({ requestFunc = "SetLabel", meter = meterName, label = newLabel })
            if response == "Success" then
                print("Label updated successfully!")
                meterData.label = newLabel -- Update local data
            else
                print("Failed to update label.")
            end
            sleep(1)
        elseif choice == 2 then
            print("Enter relay peripheral name:")
            local relay = read()
            print("Enter relay side (e.g., 'left', 'right'):")
            local side = read()
            local response = serverRequest({ requestFunc = "ConfigureMeter", meter = meterName, relay = relay, side = side })
            if response == "Success" then
                print("Configuration updated successfully!")
                meterData.redstoneConfig = { relay = relay, side = side }
            else
                print("Failed to update configuration.")
            end
            sleep(1)
        elseif choice == 3 then
            print("Enter account name to assign:")
            local accountName = read()
            local response = serverRequest({ requestFunc = "AssignAccount", meter = meterName, account = accountName })
            if response == "Success" then
                 print("Account assigned successfully!")
                 meterData.account = accountName
            else
                 print("Failed to assign account: " .. tostring(response))
            end
            sleep(2)
        elseif choice == 4 then
            break
        end
    end
end

-- Account Management Functions
local function listAccounts()
    while true do
        printHeader("List Accounts")
        local accounts = serverRequest({ requestFunc = "ListAccounts" })
        if not accounts then return end

        local accountNames = {}
        for name, _ in pairs(accounts) do
            table.insert(accountNames, name)
        end
        table.sort(accountNames)

        if #accountNames == 0 then
            print("No accounts found.")
            sleep(2)
            return
        end

        printHeader("Select an Account")
        for i, name in ipairs(accountNames) do
            print(i .. ". " .. name)
        end
        print((#accountNames + 1) .. ". Back")

        local choice = showMenu({})
        if choice == #accountNames + 1 or choice == nil then
            break
        elseif choice > 0 and choice <= #accountNames then
            viewAccount(accountNames[choice])
        end
    end
end

viewAccount = function(accountName)
    while true do
        -- We must re-request the account list each time to get the latest balance.
        local accounts = serverRequest({requestFunc = "ListAccounts"})
        if not accounts or not accounts[accountName] then
           print("Could not retrieve account details.")
           sleep(2)
           return
        end
        local account = accounts[accountName]

        printHeader("Account Details: " .. accountName)
        print("Balance: " .. string.format("%.2f", account.balance or 0) .. " Diamonds")
        print("Energy Remaining (est): " .. string.format("%.0f", account.energyRemaining or 0) .. " FE")
        print("Total Energy Used: " .. string.format("%.0f", account.energyUsed or 0) .. " FE")
        print("Energy Used Since Top-up: " .. string.format("%.0f", account.energyUsedSinceTopUp or 0) .. " FE")
        print("----------------------------------------")
        print("1. Top Up Account")
        print("2. Back")

        local choice = showMenu({})

        if choice == 1 then
            print("Enter amount to top up (in Diamonds):")
            local amountStr = read()
            local amount = tonumber(amountStr)
            if amount and amount > 0 then
                local newBalance = serverRequest({ requestFunc = "TopUp", name = accountName, amount = amount })
                if newBalance then
                    print("Top up successful!")
                else
                    print("Top up failed.")
                end
            else
                print("Invalid input. Please enter a positive number.")
            end
            sleep(2)
        elseif choice == 2 then
            break
        end
    end
end

local function createAccount()
    printHeader("Create Account")
    print("Enter new account name:")
    local name = read()
    if name and #name > 0 then
        local response = serverRequest({ requestFunc = "CreateAccount", name = name })
        if response == "Success" then
            print("Account '" .. name .. "' created successfully!")
        else
            print("Failed to create account: " .. tostring(response))
        end
    else
        print("Invalid name.")
    end
    sleep(2)
end

-- Main Menu
local function mainMenu()
    while true do
        printHeader("Main Menu")
        local choice = showMenu({
            "List & Manage Meters",
            "List & Manage Accounts",
            "Create New Account",
            "Exit"
        })

        if choice == 1 then
            listMeters()
        elseif choice == 2 then
            listAccounts()
        elseif choice == 3 then
            createAccount()
        elseif choice == 4 then
            term.clear()
            term.setCursorPos(1,1)
            print("Goodbye!")
            break
        end
    end
end

-- Program Start
rednet.open("top") -- Or any side
if not rednet.lookup(serverProtocol, serverHostname) then
    print("Could not find EMS server with hostname '"..serverHostname.."'")
    print("Please ensure the server is running and has the correct hostname.")
    return
end

print("Connected to EMS server.")
sleep(1)
mainMenu()
