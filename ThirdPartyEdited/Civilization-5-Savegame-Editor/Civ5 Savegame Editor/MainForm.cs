/*
Savegame editor (change gametype Singleplayer/Multiplayer) of Sid Meiers Civilization 5 Savegames.
Copyright (C) 2019  Jonas Heim
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/*
 * Created by SharpDevelop.
 * User: Jonas Heim
 * Date: 17.03.2019
 * Time: 13:53
 * 
 */
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;

namespace Civ5_Savegame_Editor
{
	/// <summary>
	/// Description of MainForm.
	/// </summary>
	public partial class MainForm : Form
	{
		private String WorkingDirectory;
		private String path_file_savegame;
		private BinaryWriter  binarywriter_savefile;
		private byte byte_setting_multiplayer_singleplayer;
		private const int offset_gametype = 44;
		private const byte setting_gametype_singleplayer = 0x0;	
		private const byte setting_gametype_multiplayer = 0x1;
		byte[] filedump;
		
		public MainForm()
		{
			//
			// The InitializeComponent() call is required for Windows Forms designer support.
			//
			InitializeComponent();
			
			WorkingDirectory = AppDomain.CurrentDomain.BaseDirectory;
			
			/* Set initial directory of File Dialog to base */
			openFileDialog_LoadFile.InitialDirectory = WorkingDirectory;
		}
		
		/* Load savegame file */
		void Button_LoadFileClick(object sender, EventArgs e)
		{
			if(DialogResult.OK == openFileDialog_LoadFile.ShowDialog())
			{
				path_file_savegame = openFileDialog_LoadFile.FileName;
				
				Debug.WriteLine("Loading file "+ path_file_savegame);
				
				/* Update working directory */
				WorkingDirectory = System.IO.Path.GetDirectoryName(path_file_savegame);
				openFileDialog_LoadFile.InitialDirectory = WorkingDirectory;
				
				/* Also set directory for SaveAs and enable the buttons */
				saveFileDialog_SaveAs.InitialDirectory = WorkingDirectory;
				
				/* Read Settings and set UI */
				
				try
				{
					/* Read File */
					filedump = File.ReadAllBytes(path_file_savegame);
					
					if(offset_gametype <= filedump.Length)
					{
						byte_setting_multiplayer_singleplayer = filedump[offset_gametype];
					
						/* Set RadioButtons */
						if(	(setting_gametype_singleplayer == byte_setting_multiplayer_singleplayer) || 
							(setting_gametype_multiplayer == byte_setting_multiplayer_singleplayer) )
						{
							/* Game type is valid */
							if(setting_gametype_singleplayer == byte_setting_multiplayer_singleplayer)
							{
								/* Game is a Singleplayer game */
								radioButton_GameType_Singleplayer.Checked = true;
							}
							else
							{
								/* Game is a Multiplayer game */
								radioButton_GameType_Multiplayer.Checked = true;
							}
						}
						else
						{
							/* File is something else... */
							Debug.WriteLine("Warning! - Unrecognized game type - 0x{0:X}", byte_setting_multiplayer_singleplayer);
							
							/* Notify user */
							MessageBox.Show("Warning! - Unrecognized game type", "Warning!", MessageBoxButtons.OK);
						}
						
						Debug.WriteLine("Game Type Setting - 0x{0:X}", byte_setting_multiplayer_singleplayer);
					}
					else
					{
						Debug.WriteLine("Warning! - Savegame file too small - 0x{0:X}", filedump.Length);
						/* Notify user */
						MessageBox.Show("Warning! - Savegame file too small!", "Warning!", MessageBoxButtons.OK);
					}

					/* Enable settings and saving */
					button_Save.Enabled = true;
					button_SaveAs.Enabled = true;
					groupBox_Settings.Enabled = true;
				}
				catch(Exception exception)
				{
					
				}
				
			}
		}
		void Button_SaveAsClick(object sender, EventArgs e)
		{
			if(DialogResult.OK == saveFileDialog_SaveAs.ShowDialog())
			{
				try
				{
					/* write filedump to file */
					path_file_savegame = saveFileDialog_SaveAs.FileName;
					
					File.WriteAllBytes(path_file_savegame, filedump);
				}
				catch(ArgumentNullException exception)
				{
					MessageBox.Show("Filename not valid!", "Error",  MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
				}
			}
		}
		void Button_SaveClick(object sender, EventArgs e)
		{
			try
			{
				/* save file dump to file */
				File.WriteAllBytes(path_file_savegame, filedump);	
			}
			catch(Exception exception)
			{
				
			}			
		}
		void RadioButton_GameType_SingleplayerCheckedChanged(object sender, EventArgs e)
		{
			if(true == radioButton_GameType_Singleplayer.Checked)
			{
				/* set game type in file dump */
				if(offset_gametype <= filedump.Length)
				{
					filedump[offset_gametype] = setting_gametype_singleplayer;
				}				
			}
		}
		void RadioButton_GameType_MultiplayerCheckedChanged(object sender, EventArgs e)
		{
			if(true == radioButton_GameType_Multiplayer.Checked)
			{
				/* set game type in file dump */
				if(offset_gametype <= filedump.Length)
				{
					filedump[offset_gametype] = setting_gametype_multiplayer;
				}				
			}
		}
	}
}
