unit emc2301_display;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  TAGraph, TASeries, TASources,
  Menus, emc2301_pyth_util, rpm_source, PythonEngine;

  { TForm_emc2301 }

 type

  TForm_emc2301 = class(TForm)
    Button1: TButton;
    CB_CONF_DER_OPT: TComboBox;
    CB_CONF_GAIND1: TComboBox;
    CB_CONF_GAIND2: TComboBox;
    CB_CONF_GAINI: TComboBox;
    CB_CONF_ERR_RNG: TComboBox;
    CB_CONF_GAINI1: TComboBox;
    CB_CONF_GAINI2: TComboBox;
    CB_CONF_GAINP1: TComboBox;
    CB_CONF_GAINP2: TComboBox;
    CB_CONF_MASK: TComboBox;
    CB_CONF_DIS_TO: TComboBox;
    CB_CONF_GLITCH_EN: TComboBox;
    CB_CONF_GAIND: TComboBox;
    CB_CONF_WD_EN: TComboBox;
    CB_CONF_DR_EXT_CLK: TComboBox;
    CB_CONF_USE_EXT_CLK: TComboBox;
    CB_CONF_EN_ALGO: TComboBox;
    CB_CONF_RANGE: TComboBox;
    CB_CONF_EDGES: TComboBox;
    CB_CONF_UPDATE: TComboBox;
    CB_CONF_EN_RRC: TComboBox;
    CB_CONF_GAINP: TComboBox;
    GroupBox_CONF: TGroupBox;
    GroupBox_GAIN: TGroupBox;
    GroupBox_SPINUP: TGroupBox;
    GroupBox_FANSTAT: TGroupBox;
    L_CONF_DER_OPT: TLabel;
    L_CONF_GAIND1: TLabel;
    L_CONF_GAIND2: TLabel;
    L_CONF_GAINI: TLabel;
    L_CONF_ERR_RNG: TLabel;
    L_CONF_GAINI1: TLabel;
    L_CONF_GAINI2: TLabel;
    L_CONF_GAINP1: TLabel;
    L_CONF_GAINP2: TLabel;
    L_CONF_MASK: TLabel;
    L_CONF_DIS_TO: TLabel;
    L_CONF_GLITCH_EN: TLabel;
    L_CONF_GAIND: TLabel;
    L_CONF_WD_EN: TLabel;
    L_CONF_DR_EXT_CLK: TLabel;
    L_CONF_USE_EXT_CLK: TLabel;
    L_CONF_EN_ALGO: TLabel;
    L_CONF_RANGE: TLabel;
    L_CONF_EDGES: TLabel;
    L_CONF_UPDATE: TLabel;
    L_CONF_EN_RRC: TLabel;
    L_CONF_GAINP: TLabel;
    MainMenu_emc2301: TMainMenu;
    Creator: TMenuItem;
    Help: TMenuItem;
    Graph: TMenuItem;
    PythonEngine_emc2301: TPythonEngine;
    PythonInputOutput_emc2301: TPythonInputOutput;
    procedure CB_CONF_EN_RRCChange(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure GraphClick(Sender: TObject);
    procedure L_CONF_DIS_TOClick(Sender: TObject);
    procedure PythonInputOutput_emc2301SendData(Sender: TObject;
      const Data: AnsiString);
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

uses emc2301_read, emc2301_graph;

{ TForm_emc2301 }

const
  RPM_FILE = 'rpm.txt';
  cPyLibraryLinux = 'libpython3.7m.so.1.0';
  PASSED = 0;
  FAILED = 1;
  N = 10000;
  MIN = 0;
  MAX = 10001;

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
var
  x: Double;
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

end;

procedure TForm_emc2301.CB_CONF_EN_RRCChange(Sender: TObject);
begin

end;

procedure TForm_emc2301.GraphClick(Sender: TObject);
begin
  Form_graph.Show;
end;

procedure TForm_emc2301.L_CONF_DIS_TOClick(Sender: TObject);
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
{   'READ_MEASURE':
     read_measure_emc(emc);
   'READ_MEASURE_ERR':
     writeln('read_measure_err');
   'WRITE_REG_CONF':
     writeln('Success write to CONF Register'); }
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

end.
