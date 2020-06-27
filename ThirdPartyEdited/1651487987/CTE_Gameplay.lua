-- CME_Gameplay
-- Author: Zur13
-- DateCreated: 2/9/2019 9:29:22 PM
--------------------------------------------------------------

local EAST = "EAST";
local SEAST = "SEAST";
local SWEST = "SWEST";

local FDIR_EAST = "FDIR_EAST";
local FDIR_SEAST = "FDIR_SEAST";
local FDIR_SWEST = "FDIR_SWEST";

local terTypeToIdx = nil;
local feaTypeToIdx = nil;
local resTypeToIdx = nil;
local impTypeToIdx = nil;

--******************************************************************************
-- is Expansion 2 Gathering Storm active
local function IsXP2()
	if ( GameInfo.Units_XP2 ~= nil ) then
		--print("Expansion 2 detected");
		return true;
	end
	--print("Expansion 1/none detected");
	return false;
end

--******************************************************************************
local function popTerTypeToIdx()
	if terTypeToIdx == nil then
		terTypeToIdx = {};
		for type in GameInfo.Terrains() do
			terTypeToIdx[type.TerrainType] = type.Index;
		end
	end
end

--******************************************************************************
local function popFeaTypeToIdx()
	if feaTypeToIdx == nil then
		feaTypeToIdx = {};
		for type in GameInfo.Features() do
			feaTypeToIdx[type.FeatureType] = type.Index;
		end
	end
end

--******************************************************************************
local function popResTypeToIdx()
	if resTypeToIdx == nil then
		resTypeToIdx = {};
		for type in GameInfo.Resources() do
			resTypeToIdx[type.ResourceType] = type.Index;
		end
	end
end

--******************************************************************************
local function popImpTypeToIdx()
	if impTypeToIdx == nil then
		impTypeToIdx = {};
		for type in GameInfo.Improvements() do
			impTypeToIdx[type.ImprovementType] = type.Index;
		end
	end
end

--******************************************************************************
-- table example is GameInfo.Improvements()
local function IsDbTableContains(table, col1, col1Val, col2, col2Val)
	for row in table do
		if row[col1] == col1Val and row[col2] == col2Val then
			return true;
		end
	end

	return false;
end

--******************************************************************************
-- table example is GameInfo.Improvements()
local function IsDbTableContainsAny(table, col1, col1Val)
	for row in table do
		if row[col1] == col1Val then
			return true;
		end
	end

	return false;
end

--******************************************************************************
local function isImprovementChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixParam)
	local res = true;
	local logPrefix = logPrefixParam;
	local logPrefixN;
	if logPrefix == nil then
		logPrefix = "";
	else 
		logPrefix = logPrefix .. "";
	end
	logPrefixN = logPrefix .. "   ";
	logPrefix = logPrefix .. "isImprovementChangeAllowed( )\t\t";
	print( logPrefix, " Start" );

	local logReason = "";
	local locReason = "";

	local plot = Map.GetPlotByIndex(plotId);
		
	if plot == nil then
		res = false;
	else	
		if isSafeBase or isSafeAdv then
			if impType ~= nil then
				if res and plot:IsCity() then
					logReason = " DENIED. Changes under city center are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_CITYCENTR" ;
					res = false;
				end

				if res and plot:GetWonderType() ~= nil and plot:GetWonderType() ~= -1 then
					logReason =  " DENIED. Changes under wonder buildings are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_WONDER" ;
					res = false;
				end

				if res and plot:GetDistrictType() ~= nil and plot:GetDistrictType() ~= -1 then
					logReason = " DENIED. Changes under district are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_DISTR" ;
					res = false;
				end
			end
		end

		if res and isSafeBase then
			if res and impType ~= -1 and impType ~= nil and ( not plot:IsOwned() ) then
				local impDesc = GameInfo.Improvements[impType];
				local iType = impDesc.ImprovementType;
				if not impDesc.CanBuildOutsideTerritory and iType ~= "IMPROVEMENT_BARBARIAN_CAMP" and iType ~= "IMPROVEMENT_GOODY_HUT" then
					logReason = " DENIED. Selected improvement can only be placed on owned tile. ";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_OWNED_TILE" ;
					res = false;
				end
			end

			if impType ~= nil and impType ~= -1 then

				local ter = nil;
				if terType ~= nil and terType ~= -1 then
					ter = GameInfo.Terrains[terType];
				end

				local fea = nil;
				if feaType ~= nil and feaType ~= -1 then
					fea = GameInfo.Features[feaType];
				end

				local rest = nil;
				if resType ~= nil and resType ~= -1 then
					rest = GameInfo.Resources[resType];
				end

				local imp = nil;
				if impType ~= nil and impType ~= -1 then
					imp = GameInfo.Improvements[impType];
				end

				if res and fea ~= nil and fea.NaturalWonder then
					logReason = " DENIED. Improvements on natural wonder tiles are disabled.";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_IMPR_NWTILES" ;
					res = false;
				end

				if res and IsDbTableContainsAny( GameInfo.Improvement_ValidTerrains(), "ImprovementType", imp.ImprovementType ) then
					if ter ~= nil and (not IsDbTableContains( GameInfo.Improvement_ValidTerrains(), "ImprovementType", imp.ImprovementType, "TerrainType", ter.TerrainType ) ) then
						logReason = " DENIED. Invalid terrain under improvement.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_IMPR_INV_TERR" ;
						res = false;
					end
				end
				if res and IsDbTableContainsAny( GameInfo.Improvement_ValidFeatures(), "ImprovementType", imp.ImprovementType ) then
					if fea ~= nil and ( not IsDbTableContains( GameInfo.Improvement_ValidFeatures(), "ImprovementType", imp.ImprovementType, "FeatureType", fea.FeatureType ) ) then
						logReason = " DENIED. Invalid feature under improvement.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_IMPR_INV_FEA" ;
						res = false;
					end
				end
				if res and IsDbTableContainsAny( GameInfo.Improvement_ValidResources(), "ImprovementType", imp.ImprovementType ) then
					if rest ~= nil and ( not IsDbTableContains( GameInfo.Improvement_ValidResources(), "ImprovementType", imp.ImprovementType, "ResourceType", rest.ResourceType ) ) then
						logReason = " DENIED. Invalid resource under improvement.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_IMPR_INV_RES" ;
						res = false;
					end
				end
				-- TODO: improvement POLDER check valid adjacent terrains
			elseif impType == -1 then
				-- removing is always allowed

			elseif impType == nil then
				-- unchanged should be allowed because we have already checked the new terrain, feature and resource does not conflict with existing improvement or they are left unchanged (change is denied)

			end
		end -- if res and isSafeBase then
	end
	
	local logPrefixNL = "";
	if logReason ~= nil and logReason ~= "" then
		logPrefixNL = "\n" .. "                         " .. logReason;
	end
	print( logPrefix, " End  ", plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixNL );
	return res, locReason;
end

--******************************************************************************
local function isResourceChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixParam)
	local res = true;
	local logPrefix = logPrefixParam;
	local logPrefixN;
	if logPrefix == nil then
		logPrefix = "";
	else 
		logPrefix = logPrefix .. "";
	end
	logPrefixN = logPrefix .. "   ";
	logPrefix = logPrefix .. "isResourceChangeAllowed( )    \t\t";
	print( logPrefix, " Start" );
	
	local logReason = "";
	local locReason = "";

	local plot = Map.GetPlotByIndex(plotId);
		
	if plot == nil then
		res = false;
	else	
		if isSafeBase or isSafeAdv then
			if resType ~= nil then
				if res and plot:IsCity() then
					logReason = " DENIED. Changes under city center are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_CITYCENTR" ;
					res = false;
				end

				if res and plot:GetWonderType() ~= nil and plot:GetWonderType() ~= -1 then
					logReason =  " DENIED. Changes under wonder buildings are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_WONDER" ;
					res = false;
				end

				if res and plot:GetDistrictType() ~= nil and plot:GetDistrictType() ~= -1 then
					logReason = " DENIED. Changes under district are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_DISTR" ;
					res = false;
				end
			end
		end

		if res and isSafeBase then
			if resType ~= nil and resType ~= -1 then

				local ter = nil;
				if terType ~= nil and terType ~= -1 then
					ter = GameInfo.Terrains[terType];
				end

				local fea = nil;
				if feaType ~= nil and feaType ~= -1 then
					fea = GameInfo.Features[feaType];
				end

				local rest = nil;
				if resType ~= nil and resType ~= -1 then
					rest = GameInfo.Resources[resType];
				end

				local imp = nil;
				if impType ~= nil and impType ~= -1 then
					imp = GameInfo.Improvements[impType];
				end

				if res and fea ~= nil and fea.NaturalWonder then
					logReason = " DENIED. Resources on natural wonder tile is denied.";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_NWTILE" ;
					res = false;
				end
				
				-- deny place land resource on water tile and vice versa
				if res and rest ~= nil and ter ~= nil then
					if ter.Water then
						if rest.SeaFrequency == 0 and rest.Frequency ~= 0 then
							logReason = " DENIED. Resource denied on water terrain.";
							locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_WATER" ;
							res = false;
						end
					else
						if rest.SeaFrequency ~= 0 and rest.Frequency == 0 then
							logReason = " DENIED. Resource denied on non water terrain.";
							locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_NOWATER" ;
							res = false;
						end
					end
				end

				if res and IsDbTableContainsAny( GameInfo.Resource_ValidTerrains(), "ResourceType", rest.ResourceType ) then
					if ter ~= nil and (not IsDbTableContains( GameInfo.Resource_ValidTerrains(), "ResourceType", rest.ResourceType, "TerrainType", ter.TerrainType ) ) then
						logReason = " DENIED. Invalid terrain under resource. ";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_TERR" ;
						res = false;
					end
				end
				if IsDbTableContainsAny( GameInfo.Resource_ValidFeatures(), "ResourceType", rest.ResourceType ) then
					if res and fea ~= nil and ( not IsDbTableContains( GameInfo.Resource_ValidFeatures(), "ResourceType", rest.ResourceType, "FeatureType", fea.FeatureType ) ) then
						logReason = " DENIED. Invalid feature under resource.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_FEA" ;
						res = false;
					--elseif res and feaType == -1 and IsDbTableContainsAny( GameInfo.Resource_ValidFeatures(), "ResourceType", rest.ResourceType ) then
						---- no required feature under resource
						--logReason = " DENIED. No required feature under resource.";
						--res = false;
					end
				end

				if res and ( impType == nil or not isImprovementChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN) ) then
					-- deny change resource under any existing unchanged improvement or if improvement change denied and there is existing improvement
					if plot:GetImprovementType() ~= -1 then
						logReason = " DENIED. Can't change resource under improvement or if improvement change denied.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_IMPR" ;
						res = false;
					end
				end

				-- duplicate check???
				--if res and IsDbTableContainsAny( GameInfo.Resource_ValidTerrains(), "ResourceType", rest.ResourceType ) then
					--if ter ~= nil and (not IsDbTableContains( GameInfo.Resource_ValidTerrains(), "ResourceType", rest.ResourceType, "TerrainType", ter.TerrainType ) ) then
						--logReason = " DENIED. Invalid terrain under resource.";
						--locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_TERR" ;
						--res = false;
					--end
				--end
			elseif resType == -1 then

				if res and ( impType == nil or not isImprovementChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN) ) then
					-- deny change resource under any existing unchanged improvement or if improvement change denied and there is existing improvement
					if plot:GetImprovementType() ~= -1 then
						logReason = " DENIED. Can't change resource under improvement or if improvement change denied.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_RES_DENY_IMPR" ;
						res = false;
					end
				end
			elseif resType == nil then
				-- unchanged should be allowed because we have already checked the new terrain and feature does not conflict with existing resource or they are left unchanged (change is denied)

			end
		end -- if res and isSafeBase then
	end
	
	local logPrefixNL = "";
	if logReason ~= nil and logReason ~= "" then
		logPrefixNL = "\n" .. "                         " .. logReason;
	end
	print( logPrefix, " End  ", plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixNL );
	return res, locReason;
end


--******************************************************************************
local function isFeatureChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixParam)
	local res = true;
	local logPrefix = logPrefixParam;
	local logPrefixN;
	if logPrefix == nil then
		logPrefix = "";
	else 
		logPrefix = logPrefix .. "";
	end
	logPrefixN = logPrefix .. "   ";
	logPrefix = logPrefix .. "isFeatureChangeAllowed( )    \t\t";
	print( logPrefix, " Start" );
	
	local logReason = "";
	local locReason = "";

	local plot = Map.GetPlotByIndex(plotId);
		
	if plot == nil then
		res = false;
	else
		if isSafeBase or isSafeAdv then
			if feaType ~= nil then
				if res and plot:IsCity() then
					logReason = " DENIED. Changes under city center are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_CITYCENTR" ;
					res = false;
				end

				if res and plot:GetWonderType() ~= nil and plot:GetWonderType() ~= -1 then
					logReason =  " DENIED. Changes under wonder buildings are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_WONDER" ;
					res = false;
				end

				if res and plot:GetDistrictType() ~= nil and plot:GetDistrictType() ~= -1 then
					logReason = " DENIED. Changes under district are not allowed." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_DISTR" ;
					res = false;
				end
			end
		end

		if res and isSafeBase then

			if feaType ~= nil then
				local feaDesc = GameInfo.Features[feaType];
				local feaTiles = 1;
				if feaDesc ~= nil then
					feaTiles = feaDesc.Tiles;
				end
				if feaTiles > 1 then
					local aPlots = {};
					if (ExposedMembers.MOD_CME.CustomGetMultiTileFeaturePlotList(plot, feaType, aPlots)) then
						for aPlotIdx in pairs(aPlots) do
							local aPlot = Map.GetPlotByIndex(aPlotIdx);
							if res and aPlot ~= nil then
			
								if res and plot:IsCity() then
									logReason = " DENIED. Changes under city center are not allowed (multi tile natural wonder)." ;
									locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_CITYCENTR" ;
									res = false;
								end

								if res and plot:GetWonderType() ~= nil and plot:GetWonderType() ~= -1 then
									logReason =  " DENIED. Changes under wonder buildings are not allowed (multi tile natural wonder)." ;
									locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_WONDER" ;
									res = false;
								end

								if res and plot:GetDistrictType() ~= nil and plot:GetDistrictType() ~= -1 then
									logReason = " DENIED. Changes under district are not allowed (multi tile natural wonder)." ;
									locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_DISTR" ;
									res = false;
								end
							end
						end
					end
				end
			end

			if feaType ~= nil and feaType ~= -1 then

				local ter = nil;
				if terType ~= nil and terType ~= -1 then
					ter = GameInfo.Terrains[terType];
				end

				local fea = nil;
				if feaType ~= nil and feaType ~= -1 then
					fea = GameInfo.Features[feaType];
				end

				local rest = nil;
				if resType ~= nil and resType ~= -1 then
					rest = GameInfo.Resources[resType];
				end

				local imp = nil;
				if impType ~= nil and impType ~= -1 then
					imp = GameInfo.Improvements[impType];
				end

				if res and fea ~= nil and ( fea.FeatureType == "FEATURE_VOLCANO" or fea.FeatureType == "FEATURE_KILIMANJARO" or fea.FeatureType == "FEATURE_VESUVIUS" or fea.FeatureType == "FEATURE_EYJAFJALLAJOKULL") then
					logReason = " DENIED. Mod does not allow to change volcanoes." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_VOLC" ;
					res = false;
				end

				if res and ( impType == nil or not isImprovementChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
					-- deny change feature under any existing unchanged improvement or if improvement change denied and there is existing improvement
					if plot:GetImprovementType() ~= -1 then
						logReason = " DENIED. Can't change feature under improvement or if improvement change denied.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_IMPR" ;
						res = false;
					end
				end

				if res and ( resType == nil or not isResourceChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
					-- deny change feature under unchanged resource which does not allow new feature
					if not isResourceChangeAllowed( plotId, terType, feaType, plot:GetResourceType(), impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) then
						-- deny change feature because current resource should be unchanged but it is denied on new feature
						logReason = " DENIED. Can't change feature because current resource should be unchanged but it is denied on new feature.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_RES" ;
						res = false;
					end
				end
				
				if res and IsDbTableContainsAny( GameInfo.Feature_ValidTerrains(), "FeatureType", fea.FeatureType ) then
					if ter ~= nil and (not IsDbTableContains( GameInfo.Feature_ValidTerrains(), "FeatureType", fea.FeatureType, "TerrainType", ter.TerrainType ) ) then
						logReason = " DENIED. Invalid terrain under feature.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_TERR" ;
						res = false;
					end
				end
			elseif feaType == -1 then
			
				local feaC = nil;
				local feaTypeC = plot:GetFeatureType();
				if feaTypeC ~= nil and feaTypeC ~= -1 then
					feaC = GameInfo.Features[feaTypeC];
				end

				if res and feaC ~= nil and ( feaC.FeatureType == "FEATURE_VOLCANO" or feaC.FeatureType == "FEATURE_KILIMANJARO" or feaC.FeatureType == "FEATURE_VESUVIUS" or feaC.FeatureType == "FEATURE_EYJAFJALLAJOKULL") then
					logReason = " DENIED. Mod does not allow to remove volcanoes." ;
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_VOLC_REM" ;
					res = false;
				end

				if res and ( impType == nil or not isImprovementChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
					-- deny change feature under any existing unchanged improvement or if improvement change denied and there is existing improvement
					if plot:GetImprovementType() ~= -1 then
						logReason = " DENIED. Can't change feature under improvement or if improvement change denied.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_IMPR" ;
						res = false;
					end
				end

				if res and ( resType == nil or not isResourceChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
					-- deny change feature under unchanged resource which does not allow new feature
					if not isResourceChangeAllowed( plotId, terType, feaType, plot:GetResourceType(), impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) then
						-- deny change feature because current resource should be unchanged but it is denied on new feature
						logReason = " DENIED. Can't change feature because current resource should be unchanged but it is denied on new feature.";
						locReason = "LOC_CHEAT_MAP_EDITOR_VALID_FEA_DENY_RES" ;
						res = false;
					end
				end

			elseif feaType == nil then
				-- unchanged should be allowed because we have already checked the new terrain and it does not conflict with existing resource or they are left unchanged (change is denied)

			end
		end -- if res and isSafeBase then
	end
	
	local logPrefixNL = "";
	if logReason ~= nil and logReason ~= "" then
		logPrefixNL = "\n" .. "                         " .. logReason;
	end
	print( logPrefix, " End  ", plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixNL );
	return res, locReason;
end

--******************************************************************************
local function isTerrainChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixParam)
	local res = true;
	local logPrefix = logPrefixParam;
	local logPrefixN;
	if logPrefix == nil then
		logPrefix = "";
	else 
		logPrefix = logPrefix .. "";
	end
	logPrefixN = logPrefix .. "   ";
	logPrefix = logPrefix .. "isTerrainChangeAllowed( )    \t\t";
	print( logPrefix, " Start" );
	
	local logReason = "";
	local locReason = "";

	local plot = Map.GetPlotByIndex(plotId);
		
	if terType == nil or plot == nil then
		res = false;
	else		
		local terTypeC  = plot:GetTerrainType();
		local feaTypeC = plot:GetFeatureType();
		local resTypeC  = plot:GetResourceType();
		local impTypeC = plot:GetImprovementType();
		
		if isSafeAdv then
			local terC = GameInfo.Terrains[terTypeC];
			local ter = GameInfo.Terrains[terType];
			
			if res and terC.Mountain and not ter.Mountain then
				logReason = " DENIED. Removing or creating mountains will cause crash on AI turn later." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_MOUNT" ;
				res = false;
			end

			if res and not terC.Mountain and ter.Mountain then
				logReason = " DENIED. Removing or creating mountains will cause crash on AI turn later." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_MOUNT" ;
				res = false;
			end

			if res and terC.Water and not ter.Water then
				logReason = " DENIED. Creating new land will cause crash on AI turn later." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_ADD_LAND" ;
				res = false;
			end

			if res and not terC.Water and ter.Water and plot:IsRiver() then
				logReason = " DENIED. Creating new water next to a river is not allowed." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_WATER_RIVER" ;
				res = false;
			end
		end

		if isSafeBase or isSafeAdv then
			
			if res and plot:IsCity() then
				logReason = " DENIED. Changes under city center are not allowed." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_CITYCENTR" ;
				res = false;
			end

			if res and plot:GetWonderType() ~= nil and plot:GetWonderType() ~= -1 then
				logReason =  " DENIED. Changes under wonder buildings are not allowed." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_WONDER" ;
				res = false;
			end

			if res and plot:GetDistrictType() ~= nil and plot:GetDistrictType() ~= -1 then
				logReason = " DENIED. Changes under district are not allowed." ;
				locReason = "LOC_CHEAT_MAP_EDITOR_VALID_DENY_DISTR" ;
				res = false;
			end
		end

		if res and isSafeBase then
			-- deny new terrain if it conflicts with existing unchanged improvements, resources or features
			if res and ( impType == nil or not isImprovementChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
				-- deny change terrain under any existing unchanged improvement or if improvement change denied and there is existing improvement
				if plot:GetImprovementType() ~= -1 then
					logReason = " DENIED. Can't change terrain under improvement or if improvement change denied.";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_IMPR" ;
					res = false;
				end
			end

			if res and ( resType == nil or not isResourceChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
				-- deny change terrain under unchanged resource which does not allow new feature
				if not isResourceChangeAllowed( plotId, terType, feaType, plot:GetResourceType(), impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) then
					-- deny change feature because current resource should be unchanged but it is denied on new feature
					logReason = " DENIED. Can't change terrain because current resource should be unchanged but it is denied on new terrain.";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_RES" ;
					res = false;
				end
			end

			if res and ( feaType == nil or not isFeatureChangeAllowed( plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) ) then
				-- deny change terrain under unchanged feature which does not allow new terain
				if not isFeatureChangeAllowed( plotId, terType, feaType, plot:GetResourceType(), impType, routeType, isSafeBase, isSafeAdv, logPrefixN ) then
					-- deny change terain because current feature should be unchanged but it is denied on new terain
					logReason = " DENIED. Can't change terrain because current feature should be unchanged but it is denied on new feature.";
					locReason = "LOC_CHEAT_MAP_EDITOR_VALID_TERR_DENY_FEA" ;
					res = false;
				end
			end

		end

	end
	
	local logPrefixNL = "";
	if logReason ~= nil and logReason ~= "" then
		logPrefixNL = "\n" .. "                         " .. logReason;
	end
	print( logPrefix, " End  ", plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv, logPrefixNL );
	return res, locReason;
end



--******************************************************************************
-- return true when need to fix game data
local function ChangePlot( plotId, terType, feaType, resType, resCnt, impType, routeType, owner, elevationType, contType, isSafeBase, isSafeAdv )
	print(" OnChangePlot: ", 1, plotId, terType, feaType, resType, impType);
	local res = false;

	local terReason = "";
	local feaReason = "";
	local resReason = "";
	local impReason = "";

	if plotId ~= nil then
		local plot = Map.GetPlotByIndex(plotId);
		if plot ~= nil then 
			--if owner ~= nil and owner ~= plot:GetOwner() then
			--	plot:SetOwner( owner ); -- function expected instead of nil
			--end

			local feaTypeC  = plot:GetFeatureType();
			
			local isTerChangeAllowed;
			isTerChangeAllowed, terReason = isTerrainChangeAllowed(plotId, terType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv);
			local resTerType = terType;
			if not isTerChangeAllowed  or terType == nil then
				resTerType = plot:GetTerrainType();
			end

			local isFeaChangeAllowed;
			isFeaChangeAllowed, feaReason = isFeatureChangeAllowed(plotId, resTerType, feaType, resType, impType, routeType, isSafeBase, isSafeAdv);
			local resFeaType = feaType;
			if not isFeaChangeAllowed or feaType == nil then
				resFeaType = plot:GetFeatureType();
			end

			local isResChangeAllowed;
			isResChangeAllowed, resReason = isResourceChangeAllowed(plotId, resTerType, resFeaType, resType, impType, routeType, isSafeBase, isSafeAdv);
			local resResType = resType;
			if not isResChangeAllowed  or resType == nil then
				resResType = plot:GetResourceType();
			end

			local isImpChangeAllowed;
			isImpChangeAllowed, impReason = isImprovementChangeAllowed(plotId, resTerType, resFeaType, resResType, impType, routeType, isSafeBase, isSafeAdv);
			local resImpType = impType;
			if not isImpChangeAllowed  or impType == nil then
				resImpType = plot:GetImprovementType();
			end

			print( "Reasons 1: ", terReason, feaReason, resReason, impReason );

			-- remove old plot settings to prevent even temporary invalid combinations
			local plot = Map.GetPlotByIndex(plotId);
			if isImpChangeAllowed and ( terType ~= nil or feaType ~= nil or resType ~= nil ) and impType ~= nil then
				ImprovementBuilder.SetImprovementType( plot, -1 );
			end

			local plot = Map.GetPlotByIndex(plotId);
			if isResChangeAllowed and ( terType ~= nil or feaType ~= nil ) and resType ~= nil then
				--local amberIdx = resTypeToIdx["RESOURCE_AMBER"];
				--if amberIdx ~= nil then
					--print( " ############# Temp change to amber ", GameInfo.Resources[amberIdx] );
					--ResourceBuilder.SetResourceType( plot, amberIdx, 1 );
				--end
				--local plot = Map.GetPlotByIndex(plotId);
				ResourceBuilder.SetResourceType( plot, -1, 0 );
			end

			local plot = Map.GetPlotByIndex(plotId);
			if isFeaChangeAllowed and ( terType ~= nil ) and feaType ~= nil then
				TerrainBuilder.SetFeatureType(plot, -1);
			end

			-- apply new plot settings
			plot = Map.GetPlotByIndex(plotId);
			if terType ~= nil and isTerChangeAllowed then
				--print(" OnChangePlot: ", 2, terType);
					
				local terTypeC  = plot:GetTerrainType();
				local terC = GameInfo.Terrains[terTypeC];
				local ter = GameInfo.Terrains[terType];
			
				if terC.Mountain ~= ter.Mountain then
					--print( logPrefix, " not allowed to flattern mountains because game will crash if settled on such tile" );
					res = true;
				end

				if terC.Water ~= ter.Water then
					--print( logPrefix, " not allowed to change water to land because game will crash if settled on such tile" );
					res = true;
				end

				TerrainBuilder.SetTerrainType(plot, terType);
				
				--print(" OnChangePlot: ", 3, terType);
			end

			plot = Map.GetPlotByIndex(plotId);
			if feaType ~= nil and isFeaChangeAllowed then
				print(" OnChangePlot: ", 4, feaType);
				
				if feaTypeC ~= -1 then
					local feaC = GameInfo.Features[feaTypeC];
					--print(" OnChangePlot: ", 442, feaC.Impassable);
					if feaC.Impassable then
						--print(" OnChangePlot: ", 443, feaC.Impassable);
						res = true; -- if old feature is impassable request fix data
					end
				end

				if feaType ~= -1 then
					local feaDesc = GameInfo.Features[feaType];

					local feaTiles = 1;
					if feaDesc ~= nil then
						feaTiles = feaDesc.Tiles;
						if feaDesc.Impassable then
							res = true;  -- if new feature is impassable request fix data
						end
					end
					--print(" OnChangePlot: ", 44, feaTiles);

					if feaTiles > 1 then
						local aPlots = {};
						if (ExposedMembers.MOD_CME.CustomGetMultiTileFeaturePlotList(plot, feaType, aPlots)) then
							-- clear all natural wonder tiles
							for k, aPlotIdx in pairs(aPlots) do
								local aPlot = Map.GetPlotByIndex(aPlotIdx);
								if aPlot ~= nil then
									ImprovementBuilder.SetImprovementType( aPlot, -1 );
									ResourceBuilder.SetResourceType( aPlot, -1, 0 );
									TerrainBuilder.SetFeatureType( aPlot, -1);
								end
							end
							-- place natural wonder
							TerrainBuilder.SetMultiPlotFeatureType( aPlots, feaType);
						end
					else
						TerrainBuilder.SetFeatureType(plot, feaType);
					end
				else
					-- remove feature
					TerrainBuilder.SetFeatureType(plot, feaType);
				end
				--print(" OnChangePlot: ", 5, feaType);
			end

			plot = Map.GetPlotByIndex(plotId);
			if resType ~= nil and isResChangeAllowed then
				--print(" OnChangePlot: ", 6, resType);
				if resType ~= -1 then
					if resCnt < 1 then
						ResourceBuilder.SetResourceType( plot, resType, 1 );
					else
						ResourceBuilder.SetResourceType( plot, resType, resCnt );
					end
					
				else
					ResourceBuilder.SetResourceType( plot, resType, 0 );
				end
				--print(" OnChangePlot: ", 7, resType);
			end

			plot = Map.GetPlotByIndex(plotId);
			if impType ~= nil and isImpChangeAllowed then
				--print(" OnChangePlot: ", 8, impType);
				--ImprovementBuilder.SetImprovementType( plot, impType, Game.GetLocalPlayer() );
				ImprovementBuilder.SetImprovementType( plot, impType, plot:GetOwner() );
			end

			plot = Map.GetPlotByIndex(plotId);
			if routeType ~= nil then
				--print(" OnChangePlot: ", 10, routeType)
				if routeType == RouteTypes.NONE or ( not plot:IsWater() and not plot:IsImpassable() ) then
					RouteBuilder.SetRouteType(plot, routeType ); -- RouteTypes.NONE
				end
				--print(" OnChangePlot: ", 11, routeType);
			end
			
			plot = Map.GetPlotByIndex(plotId);
			if elevationType ~= nil and IsXP2() then
				--print(" OnChangePlot: ", 12, elevationType);
				local cElevation = TerrainManager.GetCoastalLowlandType(plot);
				if cElevation ~= elevationType then
					print(" OnChangePlot: ", 125, elevationType, cElevation);
					TerrainBuilder.AddCoastalLowland(plot:GetIndex(), elevationType);
					--TerrainBuilder.AddRiverPlot(plot:GetIndex(), elevationType);
				end
				--print(" OnChangePlot: ", 13, elevationType, cElevation);
			end
			
			plot = Map.GetPlotByIndex(plotId);
			
			local mapContinents = Map.GetContinentsInUse();

				print(" OnChangePlot: ", 14, contType);
				local ccontType = plot:GetContinentType();
				print(" OnChangePlot contType: ", 141, contType, ccontType);
				local contType1 = contType;
				if contType1 == nil then
					if ccontType ~= -1 then
						contType1 = ccontType;
					else
						contType1 = -1;
					end
				end

				if plot:IsWater() then
					TerrainBuilder.SetContinentType(plot, contType1);
					--plot = Map.GetPlotByIndex(plotId);
					--TerrainBuilder.SetContinentType(plot, contType1);
					print(" OnChangePlot Water plot: ", 142, contType, ccontType);
				else
					if ccontType ~= contType or ccontType == -1 then
						--if mapContinents[2] ~= nil then
							--TerrainBuilder.SetContinentType(plot, mapContinents[2]);
							--plot = Map.GetPlotByIndex(plotId);
							--print(" OnChangePlot Terrain plot: ", 143, mapContinents[2]);
						--end
						if contType == -1 and mapContinents[1] ~= nil then
							TerrainBuilder.SetContinentType(plot, mapContinents[1]);
							plot = Map.GetPlotByIndex(plotId);
							print(" OnChangePlot Terrain plot: ", 144, mapContinents[1]);
						end
						if contType ~= nil and contType ~= -1 then
							TerrainBuilder.SetContinentType(plot, contType);
							print(" OnChangePlot Terrain plot: ", 145, contType, ccontType);
						end
					end
				end
				print(" OnChangePlot: ", 15, contType, ccontType);
			

		end --if plot ~= nil then 
	end -- if plotId ~= nil then
	
	--print(" OnChangePlot: ", 16, plotId, res);
	print( "Reasons 2: ", terReason, feaReason, resReason, impReason );
	return res, terReason, feaReason, resReason, impReason;
end

--******************************************************************************
local function GetRiverPlotFunctions( plotId, plotSide )
	local plot = Map.GetPlotByIndex(plotId);

	local setFunc = TerrainBuilder["SetWOfRiver"]; -- plotSide == 1
	local checkFunc = nil; -- plotSide == 1
	local checkFlowFunc = TerrainBuilder["GetRiverEFlowDirection"]; -- plotSide == 1

	if plot ~= nil then
		if plotSide == 1 then --river.EAST
			setFunc = TerrainBuilder["SetWOfRiver"]; 
			checkFunc = plot["IsWOfRiver"];
			checkFlowFunc = plot["GetRiverEFlowDirection"]; 

		elseif plotSide == 2 then --river.SEAST
			setFunc = TerrainBuilder["SetNWOfRiver"]; 
			checkFunc = plot["IsNWOfRiver"];
			checkFlowFunc = plot["GetRiverSEFlowDirection"]; 

		else -- plotSide == 3 == river.SWEST
			 setFunc = TerrainBuilder["SetNEOfRiver"]; 
			 checkFunc = plot["IsNEOfRiver"];
			 checkFlowFunc = plot["GetRiverSWFlowDirection"]; 

		end
	else
		-- plot == nil
		print("GetRiverPlotFunctions(). Plot is nil ", plotId);
	end
	return plot, setFunc, checkFunc, checkFlowFunc;
end

--******************************************************************************
-- return true when need to fix game data
-- plotSide: 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST
local function SetOfRiver(plotId, plotSide, rivId, enabled, fDir)
	local res = false;
	if plotId ~= nil then
		local plot = Map.GetPlotByIndex(plotId);
		if plot ~= nil then
			print("SetOfRiver", plotId, plotSide, enabled, fDir);
			local setFunc;
			local checkFunc;
			local checkFlowFunc;

			plot, setFunc, checkFunc, checkFlowFunc = GetRiverPlotFunctions( plotId, plotSide );

			if not enabled and checkFunc(plot) then
				-- remove existing river
				if IsXP2() then
					setFunc(plot, enabled, FlowDirectionTypes.NO_FLOWDIRECTION, -1);
				else
					setFunc(plot, enabled, FlowDirectionTypes.NO_FLOWDIRECTION);
				end
			
				plot, setFunc, checkFunc, checkFlowFunc = GetRiverPlotFunctions( plotId, plotSide );

				if not checkFunc(plot) then
					res = false;
				end
			elseif enabled 
				and (not checkFunc(plot) 
				or checkFlowFunc(plot) ~= fDir) then 
				-- add or change river
				if IsXP2() then
					setFunc(plot, enabled, fDir, rivId);
				else
					setFunc(plot, enabled, fDir);
				end
				plot, setFunc, checkFunc, checkFlowFunc = GetRiverPlotFunctions( plotId, plotSide );

				if checkFunc(plot) ~= enabled or checkFlowFunc ~= fDir then
					res = false;
				end
			end
		end
	end
	return res;
end

--******************************************************************************
-- return true when need to fix game data
local function ChangePlotRiver(plotId, river, rivId, isSafeBase, isSafeAdv )
	local res = false;
	local reasonRem = nil;
	
	if rivId == nil or rivId == -1 then
		rivId = 1;
	end

	if plotId ~= nil then
		local plot = Map.GetPlotByIndex(plotId);
		if plot ~= nil then 
		
--local RIVER_F_DIR_E = { nil, FlowDirectionTypes.FLOWDIRECTION_NORTH, FlowDirectionTypes.FLOWDIRECTION_SOUTH }; EAST SetWOfRiver
--local RIVER_F_DIR_SE = { nil, FlowDirectionTypes.FLOWDIRECTION_NORTHEAST, FlowDirectionTypes.FLOWDIRECTION_SOUTHWEST }; SEAST SetNWOfRiver
--local RIVER_F_DIR_SW = { nil, FlowDirectionTypes.FLOWDIRECTION_NORTHWEST, FlowDirectionTypes.FLOWDIRECTION_SOUTHEAST };  SWEST SetNEOfRiver

			if river then
				print("River plot update -", river.EAST, river.SEAST, river.SWEST, river.FDIR_EAST, river.FDIR_SEAST, river.FDIR_SWEST, rivId);
				reasonRem = {};

				local riverSides = {};
				
				local sides = {};
				
				local plotSideEAST  = 1; -- 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST
				local plotSideSEAST = 2; -- 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST
				local plotSideSWEST = 3; -- 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST

				local rEAST = plot:IsWOfRiver();
				local rSEAST = plot:IsNWOfRiver();
				local rSWEST = plot:IsNEOfRiver();

				--local startFromWest = true;

				table.insert( sides, { "EAST"  , "FDIR_EAST"  , rEAST  , plotSideEAST  , DirectionTypes.DIRECTION_EAST } );
				table.insert( sides, { "SEAST" , "FDIR_SEAST" , rSEAST , plotSideSEAST , DirectionTypes.DIRECTION_SOUTHEAST } );
				table.insert( sides, { "SWEST" , "FDIR_SWEST" , rSWEST , plotSideSWEST , DirectionTypes.DIRECTION_SOUTHWEST } );

				if river.SEAST == true then
					local fDir = river.FDIR_SEAST;
					if fDir == FlowDirectionTypes.FLOWDIRECTION_SOUTHWEST then
						--startFromWest = false;
						sides = {};
						table.insert( sides, { "SWEST" , "FDIR_SWEST" , rSWEST , plotSideSWEST , DirectionTypes.DIRECTION_SOUTHWEST } );
						table.insert( sides, { "SEAST" , "FDIR_SEAST" , rSEAST , plotSideSEAST , DirectionTypes.DIRECTION_SOUTHEAST } );
						table.insert( sides, { "EAST"  , "FDIR_EAST"  , rEAST  , plotSideEAST  , DirectionTypes.DIRECTION_EAST } );
					else
						
					end
				end
				
				for i, param in ipairs( sides ) do
					if river[ param[1] ] == true then
						-- add river requested
						local adjPlot = Map.GetAdjacentPlot( plot:GetX(), plot:GetY(), param[5] );
						if not isSafeBase or ( not plot:IsWater() and adjPlot ~= nil and not adjPlot:IsWater() ) then
							local fDir = river[ param[2] ];
							SetOfRiver(plotId, param[4] , rivId, true, fDir); -- plotSide: 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST
							res = true;
						else
							reasonRem[ param[1] ] = "LOC_CHEAT_MAP_EDITOR_VALID_RIV_DENY_WATER";
							--print("River plot update  ", param[1], reasonRem[ param[1] ] );
						end
					else
						-- remove river requested
						if not isSafeAdv and param[3] == true then
							SetOfRiver(plotId, param[4] , rivId, false, FlowDirectionTypes.NO_FLOWDIRECTION); -- plotSide: 1 == river.EAST; 2 == river.SEAST; 3 == river.SWEST
						elseif param[3] == true then
							reasonRem[ param[1] ] = "LOC_CHEAT_MAP_EDITOR_VALID_RIV_DENY_REM";
						end
					end
				end
			end -- river
		end
	end
	print("River plot update -", rivId, 44);
	return res, reasonRem;
end

--******************************************************************************
-- return true when need to fix game data
local function ChangePlotCliff(plotId, cliffs, isSafeBase, isSafeAdv)
	local res = false;
	local reasonRem = nil;

	if plotId ~= nil then
		local plot = Map.GetPlotByIndex(plotId);
		if plot ~= nil then 
			
			if cliffs then
				print("Cliffs plot update -", cliffs.EAST, cliffs.SEAST, cliffs.SWEST);
				reasonRem = {};
				if cliffs.EAST == true then
					local adjPlot = Map.GetAdjacentPlot( plot:GetX(), plot:GetY(), DirectionTypes.DIRECTION_EAST);
					if not isSafeBase or ( adjPlot ~= nil and plot:IsWater() ~= adjPlot:IsWater() ) then
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetWOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetWOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetWOfCliff(plot, true);
					else
						reasonRem.EAST = "LOC_CHEAT_MAP_EDITOR_VALID_CLI_DENY_LAND_WATER";
						print("Cliffs plot update  EAST -", reasonRem.EAST );
					end
				else
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetWOfCliff(plot, false);
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetWOfCliff(plot, false);
				end

				if cliffs.SEAST == true then
					local adjPlot = Map.GetAdjacentPlot(plot:GetX(), plot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
					if not isSafeBase or ( adjPlot ~= nil and plot:IsWater() ~= adjPlot:IsWater() ) then
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNWOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNWOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNWOfCliff(plot, true);
					else
						reasonRem.SEAST = "LOC_CHEAT_MAP_EDITOR_VALID_CLI_DENY_LAND_WATER";
						print("Cliffs plot update SEAST -", reasonRem.SEAST );
					end
				else
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetNWOfCliff(plot, false);
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetNWOfCliff(plot, false)
				end

				if cliffs.SWEST == true then
					local adjPlot = Map.GetAdjacentPlot(plot:GetX(), plot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
					if not isSafeBase or ( adjPlot ~= nil and plot:IsWater() ~= adjPlot:IsWater() ) then
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNEOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNEOfCliff(plot, true);
						plot = Map.GetPlotByIndex(plotId);
						TerrainBuilder.SetNEOfCliff(plot, true);
					else
						reasonRem.SWEST = "LOC_CHEAT_MAP_EDITOR_VALID_CLI_DENY_LAND_WATER";
						print("Cliffs plot update SWEST -", reasonRem.SWEST );
					end
				else
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetNEOfCliff(plot, false);
					plot = Map.GetPlotByIndex(plotId);
					TerrainBuilder.SetNEOfCliff(plot, false);
				end
			end -- cliff
		end
	end
	return res, reasonRem;
end

--******************************************************************************
local function FixGameData()
	--if TerrainBuilder.AnalyzeChokepoints ~= nil then
		--TerrainBuilder.AnalyzeChokepoints();
		--AreaBuilder.Recalculate();
		--TerrainBuilder.StampContinents();
		print(" ###### TerrainBuilder.AnalyzeChokepoints() ");
		TerrainBuilder.AnalyzeChokepoints();
	--end
end

--******************************************************************************
local function FixAreaData()
	--if TerrainBuilder.AnalyzeChokepoints ~= nil then
		--TerrainBuilder.AnalyzeChokepoints();
		print(" ###### AreaBuilder.Recalculate() ");
		AreaBuilder.Recalculate();
		--print(" ###### TerrainBuilder.StampContinents() ");
		--TerrainBuilder.StampContinents();
		--TerrainBuilder.AnalyzeChokepoints();
	--end
end

--************************************************************
function DeleteUnits(plotId)

	if plotId ~= nil then
		local plot = Map.GetPlotByIndex(plotId);
		if plot ~= nil then 
			local aUnits = Units.GetUnitsInPlot(plot);
			for i, pUnit in ipairs(aUnits) do
				Players[pUnit:GetOwner()]:GetUnits():Destroy(pUnit);
			end
		end
	end
end

--************************************************************
local function FindClosestCityByOwner( plotId, newOwner, plot, newOwnerPlayer, newOwnerCities )
	local closestCityDistance = 999999;
	local closestCity = nil;

	local pX = plot:GetX();
	local pY = plot:GetY();

	if newOwnerCities ~= nil then
		for j, city in newOwnerCities:Members() do
			local cX = city:GetX();
			local cY = city:GetY();
			local distance = Map.GetPlotDistance( pX, pY, cX, cY );

			if distance < closestCityDistance then 
				closestCityDistance = distance;
				closestCity = city;
			end
		end
	end
	
	return closestCity;
end

--************************************************************
local function GetCityForTileOwner( plotId, newOwner, plot, newOwnerPlayer, newOwnerCities )
	local res;
	local newOwnerCapital = newOwnerCities:GetCapitalCity();
	res = newOwnerCapital;
	-- newOwnerCities:GetCount();
	local closestCity = FindClosestCityByOwner( plotId, newOwner, plot, newOwnerPlayer, newOwnerCities );
	if closestCity ~= nil then
		res = closestCity;
	end
	return res;
end

--************************************************************
function ChangePlotOwner( plotId, newOwner, safeMod, safeAdvMod )
	print("ChangePlotOwner", 1, plotId, newOwner, safeMod, safeAdvMod );
	local plot = Map.GetPlotByIndex(plotId);

	if plotId ~= nil and newOwner ~= nil and plot:GetOwner() ~= newOwner then
		if newOwner ~= -1 then
			local newOwnerPlayer = Players[ newOwner ];
			local newOwnerCities = newOwnerPlayer:GetCities();
			if newOwnerCities ~= nil then
				local tileOwnerCity = GetCityForTileOwner( plotId, newOwner, plot, newOwnerPlayer, newOwnerCities );

				if plot ~= nil and tileOwnerCity ~= nil then 
					print("ChangePlotOwner", 2 );
					--WorldBuilder.CityManager():SetPlotOwner( plot:GetX(), plot:GetY(), entry.PlayerIndex, entry.ID );
					WorldBuilder.CityManager():SetPlotOwner( plot, tileOwnerCity ); 
				end
			end
		else
			if plot ~= nil then 
				print("ChangePlotOwner", 3 );
				--WorldBuilder.CityManager():SetPlotOwner( plot:GetX(), plot:GetY(), false );
				WorldBuilder.CityManager():SetPlotOwner( plot, false ); 
			end
		end
	end
	print("ChangePlotOwner", 4 );
end

--************************************************************
local function Initialize()
	print( " ################ Start Initializing Mod CME Gameplay Script... ################ " );
	
	-- populate internal data structures
	popTerTypeToIdx();
	popFeaTypeToIdx();
	popResTypeToIdx();
	popImpTypeToIdx();

	if ExposedMembers.MOD_CME == nil then
		ExposedMembers.MOD_CME = {};
	end
	ExposedMembers.MOD_CME.ChangePlot = ChangePlot;
	ExposedMembers.MOD_CME.FixGameData = FixGameData;
	ExposedMembers.MOD_CME.FixAreaData = FixAreaData;
	ExposedMembers.MOD_CME.ChangePlotRiver = ChangePlotRiver;
	ExposedMembers.MOD_CME.ChangePlotCliff = ChangePlotCliff;
	ExposedMembers.MOD_CME.DeleteUnits = DeleteUnits;
	ExposedMembers.MOD_CME.ChangePlotOwner = ChangePlotOwner;
	
	print( " ################ End Initializing Mod CME Gameplay Script... ################ " );
	LuaEvents.ModCme_GameplayInit(); -- notify listeners
end

Initialize();