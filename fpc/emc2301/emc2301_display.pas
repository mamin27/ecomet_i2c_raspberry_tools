unit emc2301_display;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  TAGraph, TASeries,
  Menus, ExtCtrls, emc2301_pyth_util, rpm_source, PythonEngine;

  { TForm_emc2301 }

 type

  TForm_emc2301 = class(TForm)
    BitBtn_MON: TBitBtn;
    CB_CONF_DER_OPT: TComboBox;
    CB_MON_SAMPLE: TComboBox;
    CB_SPIN_DRIVE_FAIL_CNT: TComboBox;
    CB_PWM_POLARITY: TComboBox;
    CB_PWM_BASE: TComboBox;
    CB_PWM_OUTPUT: TComboBox;
    CB_STAT_FAN_INT: TComboBox;
    CB_GN_GAINI: TComboBox;
    CB_CONF_ERR_RNG: TComboBox;
    CB_SPIN_TIME: TComboBox;
    CB_SPIN_NOKICK: TComboBox;
    CB_SPIN_LVL: TComboBox;
    CB_CONF_MASK: TComboBox;
    CB_CONF_DIS_TO: TComboBox;
    CB_CONF_GLITCH_EN: TComboBox;
    CB_GN_GAIND: TComboBox;
    CB_CONF_WD_EN: TComboBox;
    CB_CONF_DR_EXT_CLK: TComboBox;
    CB_CONF_USE_EXT_CLK: TComboBox;
    CB_CONF_EN_ALGO: TComboBox;
    CB_CONF_RANGE: TComboBox;
    CB_CONF_EDGES: TComboBox;
    CB_CONF_UPDATE: TComboBox;
    CB_CONF_EN_RRC: TComboBox;
    CB_GN_GAINP: TComboBox;
    ET_SPIN_FAN_MAX_STEP: TEdit;
    ET_STAT_FAN_SPIN: TEdit;
    ET_STAT_DRIVE_FAIL_I: TEdit;
    ET_STAT_FAN_STALL: TEdit;
    ET_STAT_WATCH: TEdit;
    ET_STAT_DRIVE_FAIL: TEdit;
    ET_TACH_COUNT: TEdit;
    ET_PWM_DIVIDE: TEdit;
    ET_ID_PRODUCT: TEdit;
    ET_ID_MANUF: TEdit;
    ET_TACH_TARGET: TEdit;
    ET_TACH_FAN_FAIL_BAND: TEdit;
    ET_TACH_READ: TEdit;
    ET_STAT_FAN_SETTING: TEdit;
    ET_SPIN_FAN_MIN_DRIVE: TEdit;
    ET_ID_REVISION: TEdit;
    GroupBox_CONF: TGroupBox;
    GroupBox_GAIN: TGroupBox;
    GroupBox_TACH: TGroupBox;
    GroupBox_SPINUP: TGroupBox;
    GroupBox_FANSTAT: TGroupBox;
    GroupBox_PWM: TGroupBox;
    GroupBox_ID: TGroupBox;
    GroupBox_Monitor: TGroupBox;
    ImageList: TImageList;
    L_CONF_DER_OPT: TLabel;
    L_SPIN_DRIVE_FAIL_CNT: TLabel;
    L_PWM_POLARITY: TLabel;
    L_TACH_COUNT: TLabel;
    L_MON_SAMPLE: TLabel;
    L_TACH_TARGET: TLabel;
    L_TACH_FAN_FAIL_BAND: TLabel;
    L_TACH_READ: TLabel;
    L_PWM_BASE: TLabel;
    L_PWM_OUTPUT: TLabel;
    L_PWM_DIVIDE: TLabel;
    L_STAT_FAN_SPIN: TLabel;
    L_STAT_FAN_STALL: TLabel;
    L_STAT_FAN_INT: TLabel;
    L_STAT_FAN_SETTING: TLabel;
    L_STAT_WATCH: TLabel;
    L_GN_GAINI: TLabel;
    L_CONF_ERR_RNG: TLabel;
    L_SPIN_TIME: TLabel;
    L_SPIN_NOKICK: TLabel;
    L_STAT_DRIVE_FAIL: TLabel;
    L_SPIN_LVL: TLabel;
    L_STAT_DRIVE_FAIL_I: TLabel;
    L_CONF_MASK: TLabel;
    L_CONF_DIS_TO: TLabel;
    L_CONF_GLITCH_EN: TLabel;
    L_GN_GAIND: TLabel;
    L_CONF_WD_EN: TLabel;
    L_CONF_DR_EXT_CLK: TLabel;
    L_CONF_USE_EXT_CLK: TLabel;
    L_CONF_EN_ALGO: TLabel;
    L_CONF_RANGE: TLabel;
    L_CONF_EDGES: TLabel;
    L_CONF_UPDATE: TLabel;
    L_CONF_EN_RRC: TLabel;
    L_GN_GAINP: TLabel;
    L_SPIN_FAN_MAX_STEP: TLabel;
    L_SPIN_FAN_MIN_DRIVE: TLabel;
    MainMenu_emc2301: TMainMenu;
    Creator: TMenuItem;
    Help: TMenuItem;
    Graph: TMenuItem;
    PythonEngine_emc2301: TPythonEngine;
    PythonInputOutput_emc2301: TPythonInputOutput;
    Timer1: TTimer;
    procedure BitBtn_MONClick(Sender: TObject);
    procedure CB_CONF_DER_OPTChange(Sender: TObject);
    procedure CB_CONF_DIS_TOChange(Sender: TObject);
    procedure CB_CONF_DR_EXT_CLKChange(Sender: TObject);
    procedure CB_CONF_EDGESChange(Sender: TObject);
    procedure CB_CONF_EN_ALGOChange(Sender: TObject);
    procedure CB_CONF_EN_RRCChange(Sender: TObject);
    procedure CB_CONF_ERR_RNGChange(Sender: TObject);
    procedure CB_CONF_GLITCH_ENChange(Sender: TObject);
    procedure CB_CONF_MASKChange(Sender: TObject);
    procedure CB_CONF_RANGEChange(Sender: TObject);
    procedure CB_CONF_UPDATEChange(Sender: TObject);
    procedure CB_CONF_USE_EXT_CLKChange(Sender: TObject);
    procedure CB_CONF_WD_ENChange(Sender: TObject);
    procedure CB_GN_GAINDChange(Sender: TObject);
    procedure CB_GN_GAINIChange(Sender: TObject);
    procedure CB_GN_GAINPChange(Sender: TObject);
    procedure CB_MON_SAMPLEChange(Sender: TObject);
    procedure CB_PWM_OUTPUTChange(Sender: TObject);
    procedure CB_PWM_POLARITYChange(Sender: TObject);
    procedure CB_PWM_BASEChange(Sender: TObject);
    procedure CB_SPIN_DRIVE_FAIL_CNTChange(Sender: TObject);
    procedure CB_SPIN_LVLChange(Sender: TObject);
    procedure CB_SPIN_NOKICKChange(Sender: TObject);
    procedure CB_SPIN_TIMEChange(Sender: TObject);
    procedure CB_STAT_FAN_INTChange(Sender: TObject);
    procedure ET_PWM_DIVIDEEditingDone(Sender: TObject);
    procedure ET_SPIN_FAN_MAX_STEPEditingDone(Sender: TObject);
    procedure ET_SPIN_FAN_MIN_DRIVEEditingDone(Sender: TObject);
    procedure ET_STAT_FAN_SETTINGEditingDone(Sender: TObject);
    procedure ET_TACH_COUNTEditingDone(Sender: TObject);
    procedure ET_TACH_FAN_FAIL_BANDEditingDone(Sender: TObject);
    procedure ET_TACH_TARGETEditingDone(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure GraphClick(Sender: TObject);
    procedure L_SPIN_FAN_MIN_DRIVEClick(Sender: TObject);
    procedure PythonInputOutput_emc2301SendData(Sender: TObject;
      const Data: AnsiString);
    procedure Timer1Timer(Sender: TObject);
  private
    procedure DoPy_InitEngine;
  public
    RPMData: TRPMArray;
  end;

var
  Form_emc2301: TForm_emc2301;
  emc: emc2301Ob;
  emc_attr: PyRecordOb;
  emc_c:  emc2301Ob_c;
  emc_c_attr: PyRecordOb_c;
  Ob_emc_c_attr: array[1..50] of PyRecordOb_c;
  ObI_emc_attr: array[1..2] of PyRecordIOb;
  Ob_emc_attr: array[1..50] of PyRecordOb;
  Ob_emc_c: array[1..50] of emc2301Ob_c;
  idx_emc_attr,idx_emc_c_attr,idx_emc_c: integer;
  test: integer;
  i: integer;

implementation

{$R *.lfm}

uses emc2301_read, emc2301_write, emc2301_graph, universal;

{ TForm_emc2301 }

const
  cPyLibraryLinux = 'libpython3.7m.so.1.0';
  PASSED = 0;
  FAILED = 1;

// WRITE Constant
  TYPE_CONF_MASK = 0;
  TYPE_CONF_DIS_TO = 1;
  TYPE_CONF_WD_EN = 2;
  TYPE_CONF_DR_EXT_CLK = 3;
  TYPE_CONF_USE_EXT_CLK = 4;
  TYPE_FAN_CONF1_EN_ALGO =5;
  TYPE_FAN_CONF1_RANGE = 6;
  TYPE_FAN_CONF1_EDGES = 7;
  TYPE_FAN_CONF1_UPDATE = 8;
  TYPE_FAN_CONF2_EN_RRC = 9;
  TYPE_FAN_CONF2_GLITCH_EN = 10;
  TYPE_FAN_CONF2_DER_OPT = 11;
  TYPE_FAN_CONF2_ERR_RNG = 12;
  TYPE_GAIN_GAIND = 13;
  TYPE_GAIN_GAINI = 14;
  TYPE_GAIN_GAINP = 15;
  TYPE_FAN_SPIN_UP_TIME =  16;
  TYPE_FAN_SPIN_UP_LVL = 17;
  TYPE_FAN_SPIN_UP_NOKICK = 18;
  TYPE_FAN_SPIN_UP_DRIVE_FAIL = 19;

  TYPE_FAN_STAT_INT = 20;
  TYPE_FAN_PWM_POLARITY = 21;
  TYPE_FAN_PWM_OUTPUT = 22;
  TYPE_FAN_PWM_BASE = 23;

// READ Constant
  TYPE_MON_SAMPLE = 100;

procedure TForm_emc2301.DoPy_InitEngine;
var
  S: string;
begin
  S:=
    {$ifdef linux} cPyLibraryLinux {$endif};
  PythonEngine_emc2301.DllPath:= ExtractFileDir(S);
  PythonEngine_emc2301.DllName:= ExtractFileName(S);
  PythonEngine_emc2301.LoadDll;
end;

procedure TForm_emc2301.FormCreate(Sender: TObject);
begin
   DoPy_InitEngine;
   emc := emc2301Ob.Init;

   for i in [1..50] do
    begin
    if i=1 then
       ObI_emc_attr[1]:= PyRecordIOb.Init
     else
       Ob_emc_attr[i]:= PyRecordOb.Init;

    Ob_emc_c[i]:= emc2301Ob_c.Init;
    Ob_emc_c_attr[i]:=PyRecordOb_c.Init;
    end;

  idx_emc_attr :=1;
  idx_emc_c_attr :=1;
  idx_emc_c :=1;
  test := FAILED;

  self_test();
  read_emc();
  Form_emc2301.Timer1.Enabled := False;
  Form_emc2301.BitBtn_MON.ImageIndex:= 0;

end;

procedure TForm_emc2301.CB_CONF_MASKChange(Sender: TObject);
begin
   write_reg_emc('CONF',EnumToChip(TYPE_CONF_MASK,Form_emc2301.CB_CONF_MASK.Items[Form_emc2301.CB_CONF_MASK.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_DIS_TOChange(Sender: TObject);
begin
   write_reg_emc('CONF',EnumToChip(TYPE_CONF_DIS_TO,Form_emc2301.CB_CONF_DIS_TO.Items[Form_emc2301.CB_CONF_DIS_TO.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_WD_ENChange(Sender: TObject);
begin
   write_reg_emc('CONF',EnumToChip(TYPE_CONF_WD_EN,Form_emc2301.CB_CONF_WD_EN.Items[Form_emc2301.CB_CONF_WD_EN.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_DR_EXT_CLKChange(Sender: TObject);
begin
   write_reg_emc('CONF',EnumToChip(TYPE_CONF_DR_EXT_CLK,Form_emc2301.CB_CONF_DR_EXT_CLK.Items[Form_emc2301.CB_CONF_DR_EXT_CLK.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_USE_EXT_CLKChange(Sender: TObject);
begin
   write_reg_emc('CONF',EnumToChip(TYPE_CONF_USE_EXT_CLK,Form_emc2301.CB_CONF_USE_EXT_CLK.Items[Form_emc2301.CB_CONF_USE_EXT_CLK.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_EN_ALGOChange(Sender: TObject);
begin
  write_reg_emc('FAN_CONF1',EnumToChip(TYPE_FAN_CONF1_EN_ALGO,Form_emc2301.CB_CONF_EN_ALGO.Items[Form_emc2301.CB_CONF_EN_ALGO.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_RANGEChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF1',EnumToChip(TYPE_FAN_CONF1_RANGE,Form_emc2301.CB_CONF_RANGE.Items[Form_emc2301.CB_CONF_RANGE.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_EDGESChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF1',EnumToChip(TYPE_FAN_CONF1_EDGES,Form_emc2301.CB_CONF_EDGES.Items[Form_emc2301.CB_CONF_EDGES.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_UPDATEChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF1',EnumToChip(TYPE_FAN_CONF1_UPDATE,Form_emc2301.CB_CONF_UPDATE.Items[Form_emc2301.CB_CONF_UPDATE.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_EN_RRCChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF2',EnumToChip(TYPE_FAN_CONF2_EN_RRC,Form_emc2301.CB_CONF_EN_RRC.Items[Form_emc2301.CB_CONF_EN_RRC.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_GLITCH_ENChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF2',EnumToChip(TYPE_FAN_CONF2_GLITCH_EN,Form_emc2301.CB_CONF_GLITCH_EN.Items[Form_emc2301.CB_CONF_GLITCH_EN.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_DER_OPTChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF2',EnumToChip(TYPE_FAN_CONF2_DER_OPT,Form_emc2301.CB_CONF_DER_OPT.Items[Form_emc2301.CB_CONF_DER_OPT.ItemIndex]));
end;

procedure TForm_emc2301.CB_CONF_ERR_RNGChange(Sender: TObject);
begin
   write_reg_emc('FAN_CONF2',EnumToChip(TYPE_FAN_CONF2_ERR_RNG,Form_emc2301.CB_CONF_ERR_RNG.Items[Form_emc2301.CB_CONF_ERR_RNG.ItemIndex]));
end;

procedure TForm_emc2301.CB_GN_GAINDChange(Sender: TObject);
begin
   write_reg_emc('GAIN',EnumToChip(TYPE_GAIN_GAIND,Form_emc2301.CB_GN_GAIND.Items[Form_emc2301.CB_GN_GAIND.ItemIndex]));
end;

procedure TForm_emc2301.CB_GN_GAINIChange(Sender: TObject);
begin
   write_reg_emc('GAIN',EnumToChip(TYPE_GAIN_GAINI,Form_emc2301.CB_GN_GAINI.Items[Form_emc2301.CB_GN_GAINI.ItemIndex]));
end;

procedure TForm_emc2301.CB_GN_GAINPChange(Sender: TObject);
begin
   write_reg_emc('GAIN',EnumToChip(TYPE_GAIN_GAINP,Form_emc2301.CB_GN_GAINP.Items[Form_emc2301.CB_GN_GAINP.ItemIndex]));
end;

procedure TForm_emc2301.CB_SPIN_TIMEChange(Sender: TObject);
begin
   write_reg_emc('FAN_SPIN_UP',EnumToChip(TYPE_FAN_SPIN_UP_TIME,Form_emc2301.CB_SPIN_TIME.Items[Form_emc2301.CB_SPIN_TIME.ItemIndex]));
end;

procedure TForm_emc2301.CB_SPIN_LVLChange(Sender: TObject);
begin
   write_reg_emc('FAN_SPIN_UP',EnumToChip(TYPE_FAN_SPIN_UP_LVL,Form_emc2301.CB_SPIN_LVL.Items[Form_emc2301.CB_SPIN_LVL.ItemIndex]));
end;

procedure TForm_emc2301.CB_SPIN_NOKICKChange(Sender: TObject);
begin
   write_reg_emc('FAN_SPIN_UP',EnumToChip(TYPE_FAN_SPIN_UP_NOKICK,Form_emc2301.CB_SPIN_NOKICK.Items[Form_emc2301.CB_SPIN_NOKICK.ItemIndex]));
end;

procedure TForm_emc2301.CB_SPIN_DRIVE_FAIL_CNTChange(Sender: TObject);
begin
   write_reg_emc('FAN_SPIN_UP',EnumToChip(TYPE_FAN_SPIN_UP_DRIVE_FAIL,Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.Items[Form_emc2301.CB_SPIN_DRIVE_FAIL_CNT.ItemIndex]));
end;

procedure TForm_emc2301.CB_STAT_FAN_INTChange(Sender: TObject);
begin
   write_reg_emc('FAN_INTERRUPT',EnumToChip(TYPE_FAN_STAT_INT,Form_emc2301.CB_STAT_FAN_INT.Items[Form_emc2301.CB_STAT_FAN_INT.ItemIndex]));
end;

procedure TForm_emc2301.ET_PWM_DIVIDEEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data: Integer;
const limit = 255;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_PWM_DIVIDE.GetTextBuf(in_buffer,Size);
   data := Trunc(PChatToReal(in_buffer,limit));
   write_reg_emc_value('PWM_DIVIDE',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.ET_SPIN_FAN_MAX_STEPEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data : Integer;
const limit = 63;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_SPIN_FAN_MAX_STEP.GetTextBuf(in_buffer,Size);
   data := Trunc(PChatToReal(in_buffer,limit));
   write_reg_emc_value('FAN_MAX_STEP',data);
   FreeMem(in_buffer, Size);
end;

procedure TForm_emc2301.ET_SPIN_FAN_MIN_DRIVEEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data: Integer;
  perc: Real;
const limit = 100;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_SPIN_FAN_MIN_DRIVE.GetTextBuf(in_buffer,Size);
   perc := Trunc(PChatToReal(in_buffer,limit));
   data := Trunc((perc * 255)/ 100);
   write_reg_emc_value('FAN_MIN_DRIVE',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.ET_STAT_FAN_SETTINGEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  perc: Real;
  data: Integer;
const limit = 100;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_STAT_FAN_SETTING.GetTextBuf(in_buffer,Size);
   perc := PChatToReal(in_buffer,limit);
   data := Trunc((perc * 255)/ 100);
   write_reg_emc_value('FAN_SETTING',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.ET_TACH_COUNTEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data: Integer;
const limit = 8160;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_TACH_COUNT.GetTextBuf(in_buffer,Size);
   data := Trunc(PChatToReal(in_buffer,limit));
   write_reg_emc_value('TACH_COUNT',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.ET_TACH_FAN_FAIL_BANDEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data: Integer;
const limit = 8191;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_TACH_FAN_FAIL_BAND.GetTextBuf(in_buffer,Size);
   data := Trunc(PChatToReal(in_buffer,limit));
   write_reg_emc_value('FAN_FAIL_BAND',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.ET_TACH_TARGETEditingDone(Sender: TObject);
var
  Size: Byte;
  in_buffer: PChar;
  data: Integer;
const limit = 8191;
begin
   Size := 20;
   GetMem(in_buffer, Size);
   Form_emc2301.ET_TACH_TARGET.GetTextBuf(in_buffer,Size);
   data := Trunc(PChatToReal(in_buffer,limit));
   write_reg_emc_value('TACH_TARGET',data);
   FreeMem(in_buffer, Size);

end;

procedure TForm_emc2301.CB_PWM_POLARITYChange(Sender: TObject);
begin
   write_reg_emc('PWM_POLARITY',EnumToChip(TYPE_FAN_PWM_POLARITY,Form_emc2301.CB_PWM_POLARITY.Items[Form_emc2301.CB_PWM_POLARITY.ItemIndex]));
end;

procedure TForm_emc2301.CB_PWM_OUTPUTChange(Sender: TObject);
begin
   write_reg_emc('PWM_OUTPUT',EnumToChip(TYPE_FAN_PWM_OUTPUT,Form_emc2301.CB_PWM_OUTPUT.Items[Form_emc2301.CB_PWM_OUTPUT.ItemIndex]));
end;

procedure TForm_emc2301.CB_PWM_BASEChange(Sender: TObject);
begin
   write_reg_emc('PWM_BASE',EnumToChip(TYPE_FAN_PWM_BASE,Form_emc2301.CB_PWM_BASE.Items[Form_emc2301.CB_PWM_BASE.ItemIndex]));
end;

procedure TForm_emc2301.CB_MON_SAMPLEChange(Sender: TObject);
var
  idx:Integer;
begin

  idx := EnumToInt(TYPE_MON_SAMPLE,Form_emc2301.CB_MON_SAMPLE.Items[Form_emc2301.CB_MON_SAMPLE.ItemIndex]);
  if idx = 0
   then Form_emc2301.Timer1.Enabled := False
   else begin
     Form_emc2301.Timer1.Interval := idx * 1000;
     Form_emc2301.Timer1.Enabled := True
   end;
end;

procedure TForm_emc2301.BitBtn_MONClick(Sender: TObject);
begin
  Form_emc2301.BitBtn_MON.ImageIndex:= 1;
  sleep(500);
  read_emc();
  read_speed();
end;

procedure TForm_emc2301.GraphClick(Sender: TObject);
begin
  Form_graph.Show;
end;

procedure TForm_emc2301.L_SPIN_FAN_MIN_DRIVEClick(Sender: TObject);
begin

end;

procedure TForm_emc2301.PythonInputOutput_emc2301SendData(Sender: TObject;
  const Data: AnsiString);
begin
  emc := StrToObj(data);

  case emc.attr1.code_type of
   'READ_emc':
     read_output_emc(emc);
   'READ_emc_ERR':
     writeln('read_emc_err');
   'READ_speed':
     read_speed_emc(emc);
   'WRITE_REG':
     begin
       writeln('Success write to Register: ', emc.attr8.attr_val_obj.attr1.attr_val);
       writeln('  Content: ', emc.attr8.attr_val_obj.attr2.attr_val);
       writeln('  Ret: ', emc.attr8.attr_val_obj.attr3.attr_val);
     end;
   'WRITE_REGVAL':
     begin
       writeln('Success write value to Register: ', emc.attr8.attr_val_obj.attr1.attr_val);
     end;
{   'GRAPH':
     begin
      LoadRPMData(RPM_FILE, RPMData);
      UserDefinedChart_RPM.PointsNumber := Length(RPMData);

      for i:=0 to N - 1 do begin
        RPM.AddXY(RPMData[i].Time,RPMData[i].RPM1);
      end;
     end;           }
   'TEST_PASSED':
     begin
       writeln('Selftest correct');
       test := PASSED;
     end;
   'MISSING_CHIP':
     begin
       writeln('Missed chip');
       test := FAILED;
  {     Form_emc2301.Deactivate;
       Application.CreateForm(TForm_missing_chip, Form_missing_chip);
       Form_missing_chip.Visible:= True;  }
     end
    else
     begin
       //writeln(emc.attr1.code_type);
       exit;
     end;
    end;
end;

procedure TForm_emc2301.Timer1Timer(Sender: TObject);
begin

  read_emc();
  read_speed();
end;

end.

