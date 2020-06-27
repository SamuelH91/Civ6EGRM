-- CTE_UI_PulldownsHelper
-- Author: Zur13
-- DateCreated: 10/13/2019 4:25:04 PM
--------------------------------------------------------------


--******************************************************************************
function UpdateNWonderList( plotId )
	if mapNaturaWonders == nil then
		mapNaturaWonders = {};
	end
	if plotId ~= nil then
		local plot = Map.GetPlotByIndex( plotId );
		if plot ~= nil then
			local curPlotNW		= plot:IsNaturalWonder();
			local curPlotFea	= plot:GetFeatureType();
			local savedMapNW	= mapNaturaWondersPlots[plotId];
			if curPlotNW == true and curPlotFea ~= savedMapNW then
				-- add/update saved map NW
				mapNaturaWondersPlots[plotId] = curPlotFea;
				--print("UpdateNWonderList. NW Added/updated in ", plotId);
			elseif curPlotNW == false and savedMapNW ~= nil then
				-- remove
				mapNaturaWondersPlots[plotId] = nil;
				--print("UpdateNWonderList. NW Removed in ", plotId);
			end
		end
	end
end

--******************************************************************************
function FindNWondersOnMap( plotId )
	if plotId ~= nil then
		local plot = Map.GetPlotByIndex( plotId );
		if plot ~= nil then
			-- update only plots in radius
			--print("Update plots in radius", 1);

			--print("Update plots in radius", 11, plotId, plot:IsNaturalWonder(), plot:GetFeatureType() );
			UpdateNWonderList( plot:GetIndex() );
			
			local radius = 5;
			local plotX = plot:GetX();
			local plotY = plot:GetY();
			for dx = -radius, radius do
				for dy = -radius,radius do
					local otherPlot = Map.GetPlotXY(plotX, plotY, dx, dy, radius);
					if otherPlot then
						--print("Update plots in radius", otherPlot:GetIndex());
						UpdateNWonderList( otherPlot:GetIndex() );
					end
				end
			end 
			--print("Update plots in radius", 2);
		end -- if plot ~= nil 
	else
		-- update all plots
		local iW, iH = Map.GetGridSize();

		plotsPendingForNWUpdate = {};
		mapNaturaWondersPlots = {};

		for i = 0, (iW * iH) - 1, 1 do
			local plot = Map.GetPlotByIndex(i);
			if plot then
				if plot:IsNaturalWonder() then
					UpdateNWonderList( plot:GetIndex() );
				end
			end
		end
	end
end

--******************************************************************************
function FindNWonders()
	mapNaturaWonders = {};
	for plotId, NWId in pairs(mapNaturaWondersPlots) do
		mapNaturaWonders[NWId] = plotId;
	end
	--print("FindNWonders");
end

--******************************************************************************
function UpdateFeaWonderExistMark()
	print(" [#UpdateFeaWonderExistMark] ", 1);
	if EntriesFea == nil then
		return;
	end
	print(" [#UpdateFeaWonderExistMark] ", 2);
	for _, entry in ipairs(EntriesFea) do 
		if entry.Type ~= nil and entry.Type ~= -1 and entry.Type ~= 0 and entry.Type.Index > -1 then
			if mapNaturaWonders[ entry.Type.Index ] ~= nil then
				print(" [#UpdateFeaWonderExistMark] ", 3);
				entry.Button:SetText(  entry.Text .. " *" );

				local tts = entry.TText;--entry.Button:GetToolTipString();
				if tts ~= nil then
					entry.Button:SetToolTipString(  tts .. "[NEWLINE]Exist on the map" );
				end
				--print("UpdateFeaWonderExistMark");
			else
				print(" [#UpdateFeaWonderExistMark] ", 4);
				entry.Button:SetText(  entry.Text );
				local tts = entry.TText;--entry.Button:GetToolTipString();
				if tts ~= nil then
					entry.Button:SetToolTipString( tts );
				end
			end
		end
	end
	print(" [#UpdateFeaWonderExistMark] ", 5);
end

--******************************************************************************
function UpdateNWondersOnPendingPlots()
	--print("UpdateNWondersOnPendingPlots()", 1);
	local processed = {};
	for i, plotId in ipairs( plotsPendingForNWUpdate ) do
		if processed[plotId] == nil then
			FindNWondersOnMap( plotId );
			processed[plotId] = plotId;
		end
	end
	plotsPendingForNWUpdate = {};
	FindNWonders();
	UpdateFeaWonderExistMark();
	--print("UpdateNWondersOnPendingPlots()", 2);
end

--******************************************************************************
-- Select all rows from table2 where table2[tbl2KeyColName] == table1[tbl1ColName] AND table1[tbl1KeyColName] == tbl1KeyColVal
-- table example is GameInfo.Improvements()
function GetAllRows( table1, table2, tbl1KeyColName, tbl1KeyColVal, tbl1ColName, tbl2KeyColName )
	local res = {};
	for row1 in table1() do
		if row1[tbl1KeyColName] == tbl1KeyColVal then
			for row2 in table2() do
				if row1[tbl1ColName] == row2[tbl2KeyColName] then
					table.insert( res, row2 );
				end
			end -- for row2 
		end -- if row1[tbl1KeyColName]
	end -- for row1 
	--print( " GetAllRows ", tbl1KeyColVal, #res );
	return res;
end

--******************************************************************************
function YieldToString( yieldType, yieldCount )
	local res = "";

	--"[ICON_FOOD]"
	--"[ICON_Production] " 
	--"[ICON_Gold] "
	--"[ICON_Science] "
	--"[ICON_Culture] " 
	--"[ICON_Faith] "
	
	res = "[" .. string.gsub( yieldType, "YIELD", "ICON" ) .. "]";
	local sign = "+";
	if yieldCount < 0 then
		sign = "-";
	end
	res = res .. " " .. sign .. yieldCount;
	return res;
end

--******************************************************************************
function BuildListTerType( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_TERRAINS_UNCH"), Type=nil });
	for type in GameInfo.Terrains() do
		local sText = Locale.Lookup(type.Name);
		if type.Water then
			sText = "[COLOR_FLOAT_SCIENCE]" .. sText .. "[ENDCOLOR]";
		elseif type.Mountain then
			sText = "[COLOR_RED]" .. sText .. "[ENDCOLOR]";
		end

		table.insert(entries, { Text=sText, Type=type });
	end

	return entries;
end

--******************************************************************************
function BuildListFea( )
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_FEATURES_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_WORLDBUILDER_NO_FEATURE"), Type=-1 });

	-- Group by 
	local NaturalWonders:table = {};
	local Other:table = {};
	
	for type in GameInfo.Features() do
		local tooltip = nil;
		if type.Description ~= nil then
			tooltip = Locale.Lookup( type.Description );
		end
		local sText = Locale.Lookup( type.Name );

		if type.NaturalWonder then
			if type.MinDistanceLand > 0 or type.MaxDistanceLand > 0 then
				sText = "[COLOR_FLOAT_SCIENCE]" .. sText .. " x " .. type.Tiles .. "[ENDCOLOR]";
			else
				sText = "[COLOR_FLOAT_FOOD]" .. sText .. " x " .. type.Tiles .. "[ENDCOLOR]";
			end
		--elseif type.ResourceClassType == "RESOURCECLASS_STRATEGIC" then
			--sText = "[COLOR_FLOAT_GOLD]" .. sText .. "[ENDCOLOR]";
			table.insert(NaturalWonders, { Text=sText, Type=type, TText = tooltip});
		else
			sText = "[COLOR_FLOAT_FAITH]" .. sText .. "[ENDCOLOR]";

			if IsXP2() then
				if type.FeatureType == "FEATURE_FLOODPLAINS" or type.FeatureType == "FEATURE_FLOODPLAINS_GRASSLAND" or type.FeatureType == "FEATURE_FLOODPLAINS_PLAINS" then
					sText = sText .. "[COLOR_RED]" .. " ! " .. "[ENDCOLOR]";
					if tooltip ~= nil then
						tooltip = tooltip .. "[NEWLINE][NEWLINE][COLOR_RED]" .. Locale.Lookup( "LOC_CHEAT_MAP_EDITOR_FEATURE_FLOODPLAINS_BUGGED" ) .. "[ENDCOLOR]";
					else
						tooltip = "[COLOR_RED]" .. Locale.Lookup( "LOC_CHEAT_MAP_EDITOR_FEATURE_FLOODPLAINS_BUGGED" ) .. "[ENDCOLOR]";
					end
				end -- if type.FeatureType 
			end -- if IsXP2() 

			table.insert(Other, { Text=sText, Type=type, TText = tooltip });
		end
	end

	-- Sort Alphabetize groups
	local sortFunc = function(a, b) 
		local aType:string = a.Text;
		local bType:string = b.Text;
		return aType < bType;
	end
	table.sort(NaturalWonders, sortFunc);
	--table.sort(Other, sortFunc);
	
	-- Collect
	for _, entry in ipairs(Other) do table.insert(entries, entry);	end;
	for _, entry in ipairs(NaturalWonders) do table.insert(entries, entry);	end;

	return entries;
end

--******************************************************************************
function BuildListRes( )
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RESOURCES_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_WORLDBUILDER_NO_RESOURCE"), Type=-1 });

	-- Group by 
	local luxu:table = {}; -- map lux resource
	local lux2:table = {}; -- minor civ lux resource
	local stra:table = {}; -- strategic resource
	local arti:table = {}; -- artifact resource
	local othe:table = {}; -- other resources (bonus)
	
	for type in GameInfo.Resources() do
		local locName = Locale.Lookup(type.Name);
		local sText = locName;
		local entry = { Text=sText, Type=type };
		local resourceType:string = type.ResourceType;
		local resourceTextIcon = "[ICON_"..resourceType.."] ";

		if type.ResourceClassType == "RESOURCECLASS_LUXURY" then
			if type.SeaFrequency > 0 then
				sText = "[COLOR_FLOAT_SCIENCE]" .. sText .. "[ENDCOLOR]";
				entry.Text = sText .. " " .. resourceTextIcon;
				table.insert(luxu, entry);
			elseif type.Frequency == 0 and type.SeaFrequency == 0 then
				-- minor civ luxury resource
				sText = "[COLOR_FLOAT_DIPLOMATIC]" .. "* " .. sText .. "[ENDCOLOR][COLOR_RED] ! [ENDCOLOR]"; -- COLOR_FLOAT_DIPLOMATIC
				entry.Text = sText .. " " .. resourceTextIcon;
				table.insert(lux2, entry);
			else
				-- map luxury resource
				sText = "[COLOR_FLOAT_GOLD]" .. sText .. "[ENDCOLOR]";
				entry.Text = sText .. " " .. resourceTextIcon;
				table.insert(luxu, entry);
			end
		elseif type.ResourceClassType == "RESOURCECLASS_STRATEGIC" then
			sText = "[COLOR_FLOAT_FOOD]" .. sText .. "[ENDCOLOR]";
			entry.Text = sText .. " " .. resourceTextIcon;
			table.insert(stra, entry);
		elseif type.ResourceClassType == "RESOURCECLASS_ARTIFACT" then
			sText = "[COLOR_FLOAT_DIPLOMATIC]" .. "** " .. sText .. "[ENDCOLOR][COLOR_RED] ! [ENDCOLOR]"; -- COLOR_FLOAT_DIPLOMATIC
			entry.Text = sText .. " " .. resourceTextIcon;
			table.insert(arti, entry);
		else
			if type.SeaFrequency > 0 then
				sText = "[COLOR_FLOAT_SCIENCE]" .. sText .. "[ENDCOLOR]";
			else
				sText = "[COLOR_FLOAT_FAITH]" .. sText .. "[ENDCOLOR]";
			end
			entry.Text = sText .. "   " .. resourceTextIcon;
			table.insert(othe, entry);
		end

		--table.insert(entries, { Text=sText, Type=type });

		-- --------------- TOOLTIP TEXT -----------------------------
		local ttext = locName .. "   " .. resourceTextIcon;
		
		if type.ResourceClassType == "RESOURCECLASS_ARTIFACT" then
			ttext = ttext .. "[NEWLINE][COLOR_RED]" .. Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RESOURCE_BUGGED") .. "[ENDCOLOR]";
		elseif type.Frequency == 0 and type.SeaFrequency == 0 then
			-- minor civ luxury resource
			ttext = ttext .. "[NEWLINE][COLOR_RED]" .. Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RESOURCE_MINOR_CIV") .. "[ENDCOLOR]";
		end

		local yields = {};
		for row in GameInfo.Resource_YieldChanges() do
			if row.ResourceType == type.ResourceType then
				table.insert( yields, row );
			end
		end
		if #yields > 0 then
			ttext = ttext .. "[NEWLINE][NEWLINE]" .. Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RES_TT_YIELDS") .. "[NEWLINE]";
			for i, row in ipairs( yields ) do
				ttext = ttext .. "    " .. YieldToString( row.YieldType, row.YieldChange );
				
			end
		end

		local validTerrains = GetAllRows( GameInfo.Resource_ValidTerrains, GameInfo.Terrains, "ResourceType", type.ResourceType , "TerrainType", "TerrainType" );
		if #validTerrains > 0 then
			ttext = ttext .. "[NEWLINE][NEWLINE]" .. Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RES_TT_VALID_TERRAINS");
			for i, terrain in ipairs( validTerrains ) do
				ttext = ttext .. "[NEWLINE]" .. Locale.Lookup(terrain.Name);
			end
		end

		local validFeatures = GetAllRows( GameInfo.Resource_ValidFeatures, GameInfo.Features, "ResourceType", type.ResourceType , "FeatureType", "FeatureType" );
		if #validFeatures > 0 then
			ttext = ttext .. "[NEWLINE][NEWLINE]" .. Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RES_TT_VALID_FEATURES");
			for i, feature in ipairs( validFeatures ) do
				ttext = ttext .. "[NEWLINE]" .. Locale.Lookup(feature.Name);
			end
		end

		

		entry.TText = ttext;

	end
	
	-- Sort Alphabetize groups
	local sortFunc = function(a, b) 
		local aType:string = a.Text;
		local bType:string = b.Text;
		return aType < bType;
	end
	table.sort(luxu, sortFunc);
	table.sort(lux2, sortFunc);
	table.sort(stra, sortFunc);
	table.sort(arti, sortFunc);
	table.sort(othe, sortFunc);
	
	-- Collect
	for _, entry in ipairs(stra) do table.insert(entries, entry);	end;
	for _, entry in ipairs(luxu) do table.insert(entries, entry);	end;
	for _, entry in ipairs(lux2) do table.insert(entries, entry);	end;
	for _, entry in ipairs(othe) do table.insert(entries, entry);	end;
	for _, entry in ipairs(arti) do table.insert(entries, entry);	end;

	return entries;
end

--******************************************************************************
function BuildListImp( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_IMPROVEMENT_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_WORLDBUILDER_NO_IMPROVEMENT"), Type=-1 });

	-- Group by 
	local base:table = {}; -- base improvements
	local outs:table = {}; -- improvements allowed to build outside
	local spec:table = {}; -- special civilization improvements

	for type in GameInfo.Improvements() do
		local sText = Locale.Lookup(type.Name);

		local tooltip = type.Description;
		if tooltip ~= nil then 
			tooltip = Locale.Lookup( tooltip );
			if type.ImprovementType == 'IMPROVEMENT_POLDER' or type.ImprovementType == 'IMPROVEMENT_MEKEWAP' then
				tooltip = tooltip .. "[NEWLINE][NEWLINE][COLOR_RED]" .. Locale.Lookup( "LOC_CHEAT_MAP_EDITOR_IMPROVEMENT_BUGGED" ) .. "[ENDCOLOR]";
			end
		end

		if type.ImprovementType == 'IMPROVEMENT_POLDER' or type.ImprovementType == 'IMPROVEMENT_MEKEWAP' then
			sText = sText .. " [COLOR_RED]" .. " !" .. "[ENDCOLOR]";
		end
		if type.CanBuildOutsideTerritory or type.ImprovementType == "IMPROVEMENT_BARBARIAN_CAMP" or type.ImprovementType == "IMPROVEMENT_GOODY_HUT" then
			sText = "[COLOR_RED]" .. sText .. "[ENDCOLOR]";
			table.insert(outs, { Text=sText, Type=type, TText = tooltip });
		else
			
			if type.Domain == "DOMAIN_SEA" then
				sText = "[COLOR_FLOAT_SCIENCE]" .. sText .. "[ENDCOLOR]";
			elseif type.TraitType ~= nil then
				sText = "[COLOR_FLOAT_FOOD]" .. sText .. "[ENDCOLOR]";
			else
				sText = "[COLOR_FLOAT_FAITH]" .. sText .. "[ENDCOLOR]";
			end

			if type.TraitType ~= nil then
				table.insert(spec, { Text=sText, Type=type, TText = tooltip });
			else
				table.insert(base, { Text=sText, Type=type, TText = tooltip });
			end
		end
		--table.insert(entries, { Text=sText, Type=type });
	end
	
	-- Sort Alphabetize groups
	local sortFunc = function(a, b) 
		local aType:string = a.Text;
		local bType:string = b.Text;
		return aType < bType;
	end
	table.sort(base, sortFunc);
	table.sort(outs, sortFunc);
	table.sort(spec, sortFunc);
	
	-- Collect
	for _, entry in ipairs(outs) do table.insert(entries, entry);	end;
	for _, entry in ipairs(base) do table.insert(entries, entry);	end;
	for _, entry in ipairs(spec) do table.insert(entries, entry);	end;
	
	return entries;
end

--******************************************************************************
function BuildListRoute( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_ROUTE_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_ROUTE_NONE"), Type=RouteTypes.NONE });

	for type in GameInfo.Routes() do
		table.insert(entries, { Text=Locale.Lookup(type.Name), Type=type });
	end

	return entries;
end

--******************************************************************************
function BuildListOwner( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_OWNER_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_OWNER_NONE"), Type=-1 });

	for i,type in pairs(PlayerManager.GetAliveIDs()) do
		local pID = type;
        local playerConfig:table = PlayerConfigurations[pID];
		local name = Locale.Lookup(playerConfig:GetPlayerName());
        local civTypeName = playerConfig:GetCivilizationTypeName();
		local civName:string = Locale.Lookup( GameInfo.Civilizations[civTypeName].Name );
		local civDesc:string = Locale.Lookup( GameInfo.Civilizations[civTypeName].Description );

		local player = Players[pID];
		local sText = name;
		
		if player ~= nil then
			if player:IsMajor() then
				--sText = "[COLOR_FLOAT_FOOD]" .. sText .. " (" .. civName .. ")" .. "[ENDCOLOR]";
				sText = "[COLOR_FLOAT_FOOD]" .. civName .. "[ENDCOLOR]";
			elseif player:IsBarbarian() then
				sText = "[COLOR_RED]" .. sText .. "[ENDCOLOR]";
			elseif player.IsFreeCities and player:IsFreeCities() then
				sText = "[COLOR_FLOAT_PRODUCTION]" .. sText .. "[ENDCOLOR]";
			else
				sText = "[COLOR_FLOAT_GOLD]" .. civDesc .. "[ENDCOLOR]";
			end
		end

		table.insert(entries, { Text=sText, Type=type });
	end

	return entries;
end

--******************************************************************************
function BuildListElev( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_ELEVATION_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_ELEVATION_NONE"), Type=-1 });
	for type = 0 , 2 , 1 do
		table.insert(entries, { Text= (type+1), Type=type });
	end

	return entries;
end

--******************************************************************************
function BuildListContType( )
	
	local entries = {};
	table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_CONTINENTS_UNCH"), Type=nil });
	table.insert(entries, { Text=Locale.Lookup("LOC_TOOLTIP_CONTINENT_NONE"), Type=-1 });
	--for type in GameInfo.Continents() do
		--local sText = Locale.Lookup(type.Description);
		--table.insert(entries, { Text=sText, Type=type });
	--end
	
	local mapContinents = Map.GetContinentsInUse();
	for idx, contId in ipairs(mapContinents) do
		local type = GameInfo.Continents[contId];
		local sText = Locale.Lookup(type.Description);
		table.insert(entries, { Text=sText, Type=type });
	end

	return entries;
end

--******************************************************************************
function BuildListRivers( )

	local riverNum :number = RiverManager.GetNumRivers();
		local type;
		local entries = {};
		--table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_CONTINENTS_UNCH"), Type=nil });
		table.insert(entries, { Text=Locale.Lookup("LOC_CHEAT_MAP_EDITOR_RIVER_NEW") .. " " .. riverNum, Type=riverNum });
		
		
		--local pRivers = RiverManager.EnumerateRivers();
		-- pRiver.Name
		-- pRiver.TypeID ~= riverId
		-- pRiver.Edges
		--for idx, pRiver in pairs(pRivers) do
			--local type = pRiver.TypeID;
			--local sText = type .. " " .. pRiver.Name;--Locale.Lookup(type.Description);
			--table.insert(entries, { Text=sText, Type=type });
		--end

		--local iW, iH = Map.GetGridSize();
		--for i = 0, (iW * iH) - 1, 1 do
			--plot = Map.GetPlotByIndex(i);
			--if plot and plot:IsRiver()  then
--
			--end
		--end
		for idx=0, riverNum-1 do
			local type = idx;
			local sText = type .. " ";--Locale.Lookup(type.Description);
			
			local kRiver = RiverManager.GetRiverByIndex( type );
			local str = tostring( type ); -- .. " / " .. tostring( kRiver.ID );
			local namedRiver = GameInfo.NamedRivers[ kRiver.TypeID ];

			if namedRiver ~= nil then
				 str  = "(ID: " .. str .. ") " .. Locale.Lookup(namedRiver.Name);-- string.gsub( namedRiver.NamedRiverType, "NAMED_RIVER_", "" );
				 sText = str;
			end


			table.insert(entries, { Text=sText, Type=type });
		end

	return entries;
end
