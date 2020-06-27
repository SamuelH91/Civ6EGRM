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
namespace Civ5_Savegame_Editor
{
	partial class MainForm
	{
		/// <summary>
		/// Designer variable used to keep track of non-visual components.
		/// </summary>
		private System.ComponentModel.IContainer components = null;
		private System.Windows.Forms.Label label_LoadFile;
		private System.Windows.Forms.TextBox textBox_LoadFile;
		private System.Windows.Forms.Button button_LoadFile;
		private System.Windows.Forms.Button button_Save;
		private System.Windows.Forms.Button button_SaveAs;
		private System.Windows.Forms.GroupBox groupBox_Settings;
		private System.Windows.Forms.OpenFileDialog openFileDialog_LoadFile;
		private System.Windows.Forms.SaveFileDialog saveFileDialog_SaveAs;
		private System.Windows.Forms.Label label_gametype;
		private System.Windows.Forms.Panel panel1;
		private System.Windows.Forms.RadioButton radioButton_GameType_Multiplayer;
		private System.Windows.Forms.RadioButton radioButton_GameType_Singleplayer;
		
		/// <summary>
		/// Disposes resources used by the form.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing) {
				if (components != null) {
					components.Dispose();
				}
			}
			base.Dispose(disposing);
		}
		
		/// <summary>
		/// This method is required for Windows Forms designer support.
		/// Do not change the method contents inside the source code editor. The Forms designer might
		/// not be able to load this method if it was changed manually.
		/// </summary>
		private void InitializeComponent()
		{
			this.label_LoadFile = new System.Windows.Forms.Label();
			this.textBox_LoadFile = new System.Windows.Forms.TextBox();
			this.button_LoadFile = new System.Windows.Forms.Button();
			this.button_Save = new System.Windows.Forms.Button();
			this.button_SaveAs = new System.Windows.Forms.Button();
			this.groupBox_Settings = new System.Windows.Forms.GroupBox();
			this.panel1 = new System.Windows.Forms.Panel();
			this.radioButton_GameType_Multiplayer = new System.Windows.Forms.RadioButton();
			this.radioButton_GameType_Singleplayer = new System.Windows.Forms.RadioButton();
			this.label_gametype = new System.Windows.Forms.Label();
			this.openFileDialog_LoadFile = new System.Windows.Forms.OpenFileDialog();
			this.saveFileDialog_SaveAs = new System.Windows.Forms.SaveFileDialog();
			this.groupBox_Settings.SuspendLayout();
			this.panel1.SuspendLayout();
			this.SuspendLayout();
			// 
			// label_LoadFile
			// 
			this.label_LoadFile.Location = new System.Drawing.Point(12, 9);
			this.label_LoadFile.Name = "label_LoadFile";
			this.label_LoadFile.Size = new System.Drawing.Size(116, 25);
			this.label_LoadFile.TabIndex = 0;
			this.label_LoadFile.Text = "Savegame";
			this.label_LoadFile.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
			// 
			// textBox_LoadFile
			// 
			this.textBox_LoadFile.Location = new System.Drawing.Point(12, 37);
			this.textBox_LoadFile.Name = "textBox_LoadFile";
			this.textBox_LoadFile.Size = new System.Drawing.Size(688, 26);
			this.textBox_LoadFile.TabIndex = 1;
			// 
			// button_LoadFile
			// 
			this.button_LoadFile.Location = new System.Drawing.Point(706, 37);
			this.button_LoadFile.Name = "button_LoadFile";
			this.button_LoadFile.Size = new System.Drawing.Size(123, 33);
			this.button_LoadFile.TabIndex = 2;
			this.button_LoadFile.Text = "Load File";
			this.button_LoadFile.UseVisualStyleBackColor = true;
			this.button_LoadFile.Click += new System.EventHandler(this.Button_LoadFileClick);
			// 
			// button_Save
			// 
			this.button_Save.Location = new System.Drawing.Point(734, 220);
			this.button_Save.Name = "button_Save";
			this.button_Save.Size = new System.Drawing.Size(95, 33);
			this.button_Save.TabIndex = 4;
			this.button_Save.Text = "Save";
			this.button_Save.UseVisualStyleBackColor = true;
			this.button_Save.Click += new System.EventHandler(this.Button_SaveClick);
			// 
			// button_SaveAs
			// 
			this.button_SaveAs.Location = new System.Drawing.Point(639, 220);
			this.button_SaveAs.Name = "button_SaveAs";
			this.button_SaveAs.Size = new System.Drawing.Size(89, 33);
			this.button_SaveAs.TabIndex = 5;
			this.button_SaveAs.Text = "Save As";
			this.button_SaveAs.UseVisualStyleBackColor = true;
			this.button_SaveAs.Click += new System.EventHandler(this.Button_SaveAsClick);
			// 
			// groupBox_Settings
			// 
			this.groupBox_Settings.Controls.Add(this.panel1);
			this.groupBox_Settings.Enabled = false;
			this.groupBox_Settings.Location = new System.Drawing.Point(12, 75);
			this.groupBox_Settings.Name = "groupBox_Settings";
			this.groupBox_Settings.Size = new System.Drawing.Size(817, 139);
			this.groupBox_Settings.TabIndex = 6;
			this.groupBox_Settings.TabStop = false;
			this.groupBox_Settings.Text = "Settings";
			// 
			// panel1
			// 
			this.panel1.Controls.Add(this.radioButton_GameType_Multiplayer);
			this.panel1.Controls.Add(this.radioButton_GameType_Singleplayer);
			this.panel1.Controls.Add(this.label_gametype);
			this.panel1.Location = new System.Drawing.Point(6, 25);
			this.panel1.Name = "panel1";
			this.panel1.Size = new System.Drawing.Size(145, 101);
			this.panel1.TabIndex = 2;
			// 
			// radioButton_GameType_Multiplayer
			// 
			this.radioButton_GameType_Multiplayer.Location = new System.Drawing.Point(6, 65);
			this.radioButton_GameType_Multiplayer.Name = "radioButton_GameType_Multiplayer";
			this.radioButton_GameType_Multiplayer.Size = new System.Drawing.Size(119, 24);
			this.radioButton_GameType_Multiplayer.TabIndex = 3;
			this.radioButton_GameType_Multiplayer.TabStop = true;
			this.radioButton_GameType_Multiplayer.Text = "Multiplayer";
			this.radioButton_GameType_Multiplayer.UseVisualStyleBackColor = true;
			this.radioButton_GameType_Multiplayer.CheckedChanged += new System.EventHandler(this.RadioButton_GameType_MultiplayerCheckedChanged);
			// 
			// radioButton_GameType_Singleplayer
			// 
			this.radioButton_GameType_Singleplayer.Location = new System.Drawing.Point(6, 35);
			this.radioButton_GameType_Singleplayer.Name = "radioButton_GameType_Singleplayer";
			this.radioButton_GameType_Singleplayer.Size = new System.Drawing.Size(136, 24);
			this.radioButton_GameType_Singleplayer.TabIndex = 2;
			this.radioButton_GameType_Singleplayer.TabStop = true;
			this.radioButton_GameType_Singleplayer.Text = "Singleplayer";
			this.radioButton_GameType_Singleplayer.UseVisualStyleBackColor = true;
			this.radioButton_GameType_Singleplayer.CheckedChanged += new System.EventHandler(this.RadioButton_GameType_SingleplayerCheckedChanged);
			// 
			// label_gametype
			// 
			this.label_gametype.Location = new System.Drawing.Point(3, 9);
			this.label_gametype.Name = "label_gametype";
			this.label_gametype.Size = new System.Drawing.Size(100, 23);
			this.label_gametype.TabIndex = 1;
			this.label_gametype.Text = "Game Type";
			// 
			// openFileDialog_LoadFile
			// 
			this.openFileDialog_LoadFile.FileName = "*.Civ5Save";
			this.openFileDialog_LoadFile.Filter = "Civilization 5 Savegame|*.Civ5Save";
			// 
			// saveFileDialog_SaveAs
			// 
			this.saveFileDialog_SaveAs.DefaultExt = "Civ5Save";
			this.saveFileDialog_SaveAs.Filter = "Civilization 5 Savegame|*.Civ5Save";
			// 
			// MainForm
			// 
			this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
			this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
			this.ClientSize = new System.Drawing.Size(841, 263);
			this.Controls.Add(this.groupBox_Settings);
			this.Controls.Add(this.button_SaveAs);
			this.Controls.Add(this.button_Save);
			this.Controls.Add(this.button_LoadFile);
			this.Controls.Add(this.textBox_LoadFile);
			this.Controls.Add(this.label_LoadFile);
			this.Icon = global::Civ5_Savegame_Editor.Icon.Civ5Icon;
			this.Name = "MainForm";
			this.Text = "Civ5 Savegame Editor";
			this.groupBox_Settings.ResumeLayout(false);
			this.panel1.ResumeLayout(false);
			this.ResumeLayout(false);
			this.PerformLayout();

		}
	}
}
