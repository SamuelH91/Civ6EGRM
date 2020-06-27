-- CME_WonderGen
-- Author: Yurii
-- DateCreated: 2/18/2019 7:15:16 PM
--------------------------------------------------------------


------------------------------------------------------------------------------
function CustomGetMultiTileFeaturePlotList2(pPlot, eFeatureType, aPlots)
	local disableValidation = true;
	-- First check this plot itself

	if ( not disableValidation and not TerrainBuilder.CanHaveFeature(pPlot, eFeatureType, true)) then
		print(" CustomGetMultiTileFeaturePlotList: ", 1 );
		return false;
	else
		table.insert(aPlots, pPlot:GetIndex());
	end

	-- Which type of custom placement is it?
	local customPlacement = GameInfo.Features[eFeatureType].CustomPlacement;

		-- 2 tiles inland, east-west facing camera
	if (customPlacement == "PLACEMENT_TORRES_DEL_PAINE" or
	    customPlacement == "PLACEMENT_YOSEMITE") then

		-- Assume first tile is the western one, check the one to the east
		local pAdjacentPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		if (pAdjacentPlot ~= nil 
			and ( disableValidation or TerrainBuilder.CanHaveFeature(pAdjacentPlot, eFeatureType, true) == true )
			) then
			table.insert(aPlots, pAdjacentPlot:GetIndex());
			print(" CustomGetMultiTileFeaturePlotList: ", 2 );
			return true;
		end

	-- 2 tiles on coast, roughly facing camera
	elseif (customPlacement == "PLACEMENT_CLIFFS_DOVER") then
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);

		-- W and SW are water, see if SE works
		local pSecondPlot;
		if ( disableValidation or ( pWPlot ~= nil and pSWPlot ~= nil and pWPlot:IsWater() and pWPlot:IsLake() == false and pSWPlot:IsWater() and pWPlot:IsLake() == false ) ) then
			pSecondPlot = pSEPlot;

		-- SW and SE are water, see if E works
		elseif ( disableValidation or ( pSWPlot ~= nil and pSEPlot ~= nil and pSWPlot:IsWater() and pSWPlot:IsLake() == false and pSEPlot:IsWater() and pSEPlot:IsLake() == false ) ) then
			pSecondPlot = pEPlot;

		-- SE and E are water, see if NE works
		elseif ( disableValidation or ( pSWPlot ~= nil and pEPlot ~= nil  and pSEPlot:IsWater() and pSEPlot:IsLake() == false and pEPlot:IsWater() and pEPlot:IsLake() == false ) ) then
			pSecondPlot = pNEPlot;
		
		else
			print(" CustomGetMultiTileFeaturePlotList: ", 3 );
			return false;
		end

		if ( disableValidation or TerrainBuilder.CanHaveFeature(pSecondPlot, eFeatureType, true) ) then
			table.insert(aPlots, pSecondPlot:GetIndex());
			return true;
		end

	-- 2 tiles, one on coastal land and one in water, try to face camera if possible
	elseif (customPlacement == "PLACEMENT_GIANTS_CAUSEWAY") then

		-- Assume first tile a land tile without hills, check around it in a preferred order for water
		if ( not disableValidation and ( pPlot:IsWater() or pPlot:IsHills() )) then
			print(" CustomGetMultiTileFeaturePlotList: ", 4 );
			return false;
		end

		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		if (pSWPlot ~= nil and pSWPlot:IsWater() and pSWPlot:IsLake() == false) then
			table.insert(aPlots, pSWPlot:GetIndex());
			return true;
		end

		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		if (pSEPlot ~= nil and pSEPlot:IsWater() and pSEPlot:IsLake() == false) then
			table.insert(aPlots, pSEPlot:GetIndex());
			return true;
		end

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		if (pWPlot ~= nil and pWPlot:IsWater() and pWPlot:IsLake() == false) then
			table.insert(aPlots, pWPlot:GetIndex());
			return true;
		end

		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		if (pEPlot ~= nil and pEPlot:IsWater() and pEPlot:IsLake() == false) then
			table.insert(aPlots, pEPlot:GetIndex());
			return true;
		end

		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		if (pNWPlot ~= nil and pNWPlot:IsWater() and pNWPlot:IsLake() == false) then
			table.insert(aPlots, pNWPlot:GetIndex());
			return true;
		end

		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		if (pNEPlot ~= nil and pNEPlot:IsWater() and pNEPlot:IsLake() == false) then
			table.insert(aPlots, pNEPlot:GetIndex());
			return true;
		end
		
	-- 3 tiles in triangle coast on front edge, land behind (with any rotation)
	elseif (customPlacement == "PLACEMENT_PIOPIOTAHI") then

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		
		-- all 6 hexes around must be land

		if ( not disableValidation and ( pNWPlot == nil or pNEPlot == nil or pWPlot== nil or pSWPlot== nil or pSEPlot== nil or pEPlot== nil or pNWPlot:IsWater() or pNEPlot:IsWater() or pWPlot:IsWater() or pSWPlot:IsWater() or pSEPlot:IsWater() or pEPlot:IsWater() )) then
			print(" CustomGetMultiTileFeaturePlotList: ", 5 );
			return false;
		else
			-- find two adjacent plots that can both serve for this NW
			local bWValid  = true; -- TerrainBuilder.CanHaveFeature(pWPlot, eFeatureType, true);
			local bNWValid = true; -- TerrainBuilder.CanHaveFeature(pNWPlot, eFeatureType, true);
			local bNEValid = true; -- TerrainBuilder.CanHaveFeature(pNEPlot, eFeatureType, true);
			local bEValid  = true; -- TerrainBuilder.CanHaveFeature(pEPlot, eFeatureType, true);
			local bSEValid = true; -- TerrainBuilder.CanHaveFeature(pSEPlot, eFeatureType, true);
			local bSWValid = true; -- TerrainBuilder.CanHaveFeature(pSWPlot, eFeatureType, true);

			if (bSEValid ~= nil and bSWValid ~= nil and bSEValid == true and bSWValid == true ) then
				pWaterCheck1 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 6 );
					return false;
				else
					table.insert(aPlots, pSEPlot:GetIndex());
					table.insert(aPlots, pSWPlot:GetIndex());
					return true;
				end
			end
			
			if (bEValid  ~= nil and bSEValid ~= nil and bEValid  == true and bSEValid == true ) then
				if (Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 7 );
					return false;
				elseif (Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 8 );
					return false;
				elseif ( Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 8 );
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);

				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 10 );
					return false;
				else
					table.insert(aPlots, pEPlot:GetIndex());
					table.insert(aPlots, pSEPlot:GetIndex());
					return true;
				end
			end
			
			if (bSWValid  ~= nil and bWValid ~= nil and bSWValid  == true and bWValid == true ) then
				if (Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 11 );
					return false;
				elseif (Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 12 );
					return false;
				elseif ( Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 13 );
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 14 );
					return false;
				else
					table.insert(aPlots, pSWPlot:GetIndex());
					table.insert(aPlots, pWPlot:GetIndex());
					return true;
				end
			end

			if (bWValid  ~= nil and bNWValid ~= nil and bWValid  == true and bNWValid == true ) then
				if (Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 15 );
					return false;
				elseif (Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 16 );
					return false;
				elseif ( Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 17 );
					return false;
				end
				
				pWaterCheck1 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 18 );
					return false;
				else
					table.insert(aPlots, pWPlot:GetIndex());
					table.insert(aPlots, pNWPlot:GetIndex());
					return true;
				end
			end
			
			if (bNEValid  ~= nil and bEValid ~= nil and bNEValid  == true and bEValid == true ) then
				if (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 19 );
					return false;
				elseif (Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 20 );
					return false;
				elseif ( Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 21 );
					return false;
				end
				
				pWaterCheck1 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 22 );
					return false;
				else
					table.insert(aPlots, pNEPlot:GetIndex());
					table.insert(aPlots, pEPlot:GetIndex());
					return true;
				end
			end

			if (bNWValid  ~= nil and bNEValid ~= nil and bNWValid  == true and bNEValid == true ) then
				if (Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 23 );
					return false;
				elseif (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 24 );
					return false;
				elseif (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					print(" CustomGetMultiTileFeaturePlotList: ", 25 );
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				if ( not disableValidation and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					print(" CustomGetMultiTileFeaturePlotList: ", 26 );
					return false;
				else
					table.insert(aPlots, pNWPlot:GetIndex());
					table.insert(aPlots, pNEPlot:GetIndex());
					return true;
				end
			end
		end
	else
		-- no custom placement
		local tilesCount = GameInfo.Features[eFeatureType].Tiles

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);

		if tilesCount > 1 then
			-- second tile EAST
			table.insert(aPlots, pEPlot:GetIndex());
		end
		if tilesCount > 2 then
			-- third tile NORTHEAST
			table.insert(aPlots, pNEPlot:GetIndex());
		end
		if tilesCount > 3 then
			-- third tile NORTHWEST
			table.insert(aPlots, pNWPlot:GetIndex());
		end
		return true;
	end
	print(" CustomGetMultiTileFeaturePlotList: ", 27 );
	return false;
end

------------------------------------------------------------------------------
function CustomGetMultiTileFeaturePlotList(pPlot, eFeatureType, aPlots)
	local disableValidation = true;

	if ( not disableValidation and not TerrainBuilder.CanHaveFeature(pPlot, eFeatureType, true)) then
		print(" CustomGetMultiTileFeaturePlotList: ", 1 );
		return false;
	else
		table.insert(aPlots, pPlot:GetIndex());
	end

	-- Which type of custom placement is it?
	local customPlacement = GameInfo.Features[eFeatureType].CustomPlacement;

		-- 2 tiles inland, east-west facing camera
	if (customPlacement == "PLACEMENT_TORRES_DEL_PAINE" or
	    customPlacement == "PLACEMENT_YOSEMITE") then

		-- Assume first tile is the western one, check the one to the east
		local pAdjacentPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		if (pAdjacentPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pAdjacentPlot, eFeatureType, true) == true) ) then
			table.insert(aPlots, pAdjacentPlot:GetIndex());
			return true;
		end

	-- 2 tiles on coast, roughly facing camera
	elseif (customPlacement == "PLACEMENT_CLIFFS_DOVER") then
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);

		-- W and SW are water, see if SE works
		local pSecondPlot;
		if (pWPlot ~= nil and pSWPlot ~= nil and ( disableValidation or pWPlot:IsWater() and pWPlot:IsLake() == false and pSWPlot:IsWater() and pWPlot:IsLake() == false ) ) then
			pSecondPlot = pSEPlot;

		-- SW and SE are water, see if E works
		elseif (pSWPlot ~= nil and pSEPlot ~= nil and ( disableValidation or pSWPlot:IsWater() and pSWPlot:IsLake() == false and pSEPlot:IsWater() and pSEPlot:IsLake() == false ) ) then
			pSecondPlot = pEPlot;

		-- SE and E are water, see if NE works
		elseif (pSWPlot ~= nil and pEPlot ~= nil  and ( disableValidation or pSEPlot:IsWater() and pSEPlot:IsLake() == false and pEPlot:IsWater() and pEPlot:IsLake() == false ) ) then
			pSecondPlot = pNEPlot;
		
		else
			return false;
		end

		if ( disableValidation or TerrainBuilder.CanHaveFeature(pSecondPlot, eFeatureType, true) ) then
			table.insert(aPlots, pSecondPlot:GetIndex());
			return true;
		end

	-- 2 tiles, one on coastal land and one in water, try to face camera if possible
	elseif (customPlacement == "PLACEMENT_GIANTS_CAUSEWAY") then

		-- Assume first tile a land tile without hills, check around it in a preferred order for water
		if ( (not disableValidation) and ( pPlot:IsWater() or pPlot:IsHills() ) ) then
			return false;
		end

		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		if (pSWPlot ~= nil and pSWPlot:IsWater() and pSWPlot:IsLake() == false) then
			table.insert(aPlots, pSWPlot:GetIndex());
			return true;
		end

		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		if (pSEPlot ~= nil and pSEPlot:IsWater() and pSEPlot:IsLake() == false) then
			table.insert(aPlots, pSEPlot:GetIndex());
			return true;
		end

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		if (pWPlot ~= nil and pWPlot:IsWater() and pWPlot:IsLake() == false) then
			table.insert(aPlots, pWPlot:GetIndex());
			return true;
		end

		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		if (pEPlot ~= nil and pEPlot:IsWater() and pEPlot:IsLake() == false) then
			table.insert(aPlots, pEPlot:GetIndex());
			return true;
		end

		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		if (pNWPlot ~= nil and pNWPlot:IsWater() and pNWPlot:IsLake() == false) then
			table.insert(aPlots, pNWPlot:GetIndex());
			return true;
		end

		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		if ( pNEPlot ~= nil and ( disableValidation or ( pNEPlot:IsWater() and pNEPlot:IsLake() == false ) ) ) then
			table.insert(aPlots, pNEPlot:GetIndex());
			return true;
		end
		
	-- 4 tiles (triangle plus a tail)
	--elseif (customPlacement == "PLACEMENT_RORAIMA") then
--
		---- This one does require three in a row, so let's find that first
		--for i = 0, DirectionTypes.NUM_DIRECTION_TYPES - 1, 1 do
			--local pFirstPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), i);
			--if ( pFirstPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pFirstPlot, eFeatureType, true) ) ) then
				--local pSecondPlot = Map.GetAdjacentPlot(pFirstPlot:GetX(), pFirstPlot:GetY(), i);
				--if ( pSecondPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pSecondPlot, eFeatureType, true) ) ) then
					--local iNewDir = i - 1;
					--if iNewDir == -1 then
						--iNewDir = 5;
					--end
					--local pThirdPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), iNewDir);
					--if ( pThirdPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pThirdPlot, eFeatureType, true) ) ) then
						--table.insert(aPlots, pFirstPlot:GetIndex());
						--table.insert(aPlots, pSecondPlot:GetIndex());
						--table.insert(aPlots, pThirdPlot:GetIndex());
						--return true;
					--end
				--end
			--end
		--end

	-- 3 tiles in a straight line
	elseif (customPlacement == "PLACEMENT_ZHANGYE_DANXIA") then

		for i = 0, DirectionTypes.NUM_DIRECTION_TYPES - 1, 1 do
			local pFirstPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), i);
			if ( pFirstPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pFirstPlot, eFeatureType, true) ) ) then
				local pSecondPlot = Map.GetAdjacentPlot(pFirstPlot:GetX(), pFirstPlot:GetY(), i);
				if ( pSecondPlot ~= nil and ( disableValidation or TerrainBuilder.CanHaveFeature(pSecondPlot, eFeatureType, true) ) ) then
					table.insert(aPlots, pFirstPlot:GetIndex());
					table.insert(aPlots, pSecondPlot:GetIndex());
					return true;
				end
			end
		end

	-- 3 tiles in triangle coast on front edge, land behind (with any rotation)
	elseif (customPlacement == "PLACEMENT_PIOPIOTAHI") then

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
		
		-- all 6 hexes around must be land

		if ( pNWPlot == nil or pNEPlot == nil or pWPlot== nil or pSWPlot== nil or pSEPlot== nil or pEPlot== nil or ( not disableValidation ) and ( pNWPlot:IsWater() or pNEPlot:IsWater() or pWPlot:IsWater() or pSWPlot:IsWater() or pSEPlot:IsWater() or pEPlot:IsWater() ) ) then
			return false;
		else
			-- find two adjacent plots that can both serve for this NW
			local bWValid  = ( disableValidation or TerrainBuilder.CanHaveFeature(pWPlot, eFeatureType, true) );
			local bNWValid = ( disableValidation or TerrainBuilder.CanHaveFeature(pNWPlot, eFeatureType, true) );
			local bNEValid = ( disableValidation or TerrainBuilder.CanHaveFeature(pNEPlot, eFeatureType, true) );
			local bEValid  = ( disableValidation or TerrainBuilder.CanHaveFeature(pEPlot, eFeatureType, true) );
			local bSEValid = ( disableValidation or TerrainBuilder.CanHaveFeature(pSEPlot, eFeatureType, true) );
			local bSWValid = ( disableValidation or TerrainBuilder.CanHaveFeature(pSWPlot, eFeatureType, true) );

			if (bSEValid ~= nil and bSWValid ~= nil and bSEValid == true and bSWValid == true ) then
				pWaterCheck1 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pSEPlot:GetIndex());
					table.insert(aPlots, pSWPlot:GetIndex());
					return true;
				end
			end
			
			if (bEValid  ~= nil and bSEValid ~= nil and bEValid  == true and bSEValid == true ) then
				if (Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					return false;
				elseif ( Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST) == nil) then
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pSEPlot:GetX(), pSEPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);

				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pEPlot:GetIndex());
					table.insert(aPlots, pSEPlot:GetIndex());
					return true;
				end
			end
			
			if (bSWValid  ~= nil and bWValid ~= nil and bSWValid  == true and bWValid == true ) then
				if (Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST) == nil) then
					return false;
				elseif ( Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pSWPlot:GetX(), pSWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pSWPlot:GetIndex());
					table.insert(aPlots, pWPlot:GetIndex());
					return true;
				end
			end

			if (bWValid  ~= nil and bNWValid ~= nil and bWValid  == true and bNWValid == true ) then
				if (Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_WEST) == nil) then
					return false;
				elseif ( Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					return false;
				end
				
				pWaterCheck1 = Map.GetAdjacentPlot(pWPlot:GetX(), pWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_WEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pWPlot:GetIndex());
					table.insert(aPlots, pNWPlot:GetIndex());
					return true;
				end
			end
			
			if (bNEValid  ~= nil and bEValid ~= nil and bNEValid  == true and bEValid == true ) then
				if (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					return false;
				elseif ( Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST) == nil) then
					return false;
				end
				
				pWaterCheck1 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				pWaterCheck2 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				pWaterCheck3 = Map.GetAdjacentPlot(pEPlot:GetX(), pEPlot:GetY(), DirectionTypes.DIRECTION_EAST);
				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pNEPlot:GetIndex());
					table.insert(aPlots, pEPlot:GetIndex());
					return true;
				end
			end

			if (bNWValid  ~= nil and bNEValid ~= nil and bNWValid  == true and bNEValid == true ) then
				if (Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST) == nil) then
					return false;
				elseif (Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST) == nil) then
					return false;
				end

				pWaterCheck1 = Map.GetAdjacentPlot(pNWPlot:GetX(), pNWPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				pWaterCheck2 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
				pWaterCheck3 = Map.GetAdjacentPlot(pNEPlot:GetX(), pNEPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
				if ( ( not disableValidation ) and ( pWaterCheck1:IsWater() == false or pWaterCheck2:IsWater() == false or pWaterCheck3:IsWater() == false ) ) then
					return false;
				else
					table.insert(aPlots, pNWPlot:GetIndex());
					table.insert(aPlots, pNEPlot:GetIndex());
					return true;
				end
			end
		end
	else
		-- no custom placement
		local tilesCount = GameInfo.Features[eFeatureType].Tiles

		local pWPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_WEST);
		local pNWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHWEST);
		local pNEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_NORTHEAST);
		local pEPlot  = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_EAST);
		local pSEPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHEAST);
		local pSWPlot = Map.GetAdjacentPlot(pPlot:GetX(), pPlot:GetY(), DirectionTypes.DIRECTION_SOUTHWEST);

		if tilesCount > 1 then
			-- second tile EAST
			-- * *
			table.insert(aPlots, pEPlot:GetIndex());
		end

		local wType = GameInfo.Features[eFeatureType].FeatureType;

		if tilesCount > 2 then
			-- "FEATURE_GOBUSTAN" ???
			if wType == "FEATURE_ZHANGYE_DANXIA" or wType == "FEATURE_RORAIMA" then
				-- linear
				-- * * *
				table.insert(aPlots, pWPlot:GetIndex());
			else
				-- triangle
				--  *
				-- * *
				-- third tile NORTHEAST
				table.insert(aPlots, pNEPlot:GetIndex());
			end
		end
		if tilesCount > 3 then
			-- "FEATURE_CHOCOLATEHILLS" shape ???
			-- "FEATURE_WHITEDESERT" shape ???
			if wType == "FEATURE_RORAIMA" then
				-- L-shape 
				-- * * *
				--    *
				-- 4-th tile SOUTHWEST
				table.insert(aPlots, pSEPlot:GetIndex());
			else
				-- rhombus
				--  * *
				-- * *
				-- 4-th tile NORTHWEST
				table.insert(aPlots, pNWPlot:GetIndex());
			end
		end
		return true;
	end

	return false;
end

--************************************************************
local function Initialize()
	print( " ################ Start Initializing Mod CME WonderGen Script... ################ " );

	if ExposedMembers.MOD_CME == nil then
		ExposedMembers.MOD_CME = {};
	end
	ExposedMembers.MOD_CME.CustomGetMultiTileFeaturePlotList = CustomGetMultiTileFeaturePlotList;
	
	print( " ################ End Initializing Mod CME WonderGen Script... ################ " );
end

Initialize();