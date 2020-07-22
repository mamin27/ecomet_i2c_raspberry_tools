unit hdc1080_display;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  proc_py,hdc1080_pyth_util,math,
  PythonEngine;

type

  { TForm_hdc1080 }

  TForm_hdc1080 = class(TForm)
    BitBtn_setting: TBitBtn;
    ComboBox_mode: TComboBox;
    ComboBox_temp: TComboBox;
    ComboBox_hmdt: TComboBox;
    ComboBox_heating: TComboBox;
    Edit_manuf: TEdit;
    Edit_devid: TEdit;
    Edit_temp: TEdit;
    Edit_hmdt: TEdit;
    Edit_serial: TEdit;
    GroupBox_accuracy: TGroupBox;
    GroupBox_settings: TGroupBox;
    GroupBox_measure_box: TGroupBox;
    ImageList_hdc1080: TImageList;
    Label_mid: TLabel;
    Label_heating: TLabel;
    Label_mode: TLabel;
    Label_temp: TLabel;
    Label_hmdt: TLabel;
    Label_mtemp: TLabel;
    Label_mhmdt: TLabel;
    PythonEngine_hdc1080: TPythonEngine;
    PythonInputOutput_hdc1080: TPythonInputOutput;
    procedure BitBtn_settingClick(Sender: TObject);
    procedure ComboBox_heatingChange(Sender: TObject);
    procedure ComboBox_hmdtChange(Sender: TObject);
    procedure ComboBox_modeChange(Sender: TObject);
    procedure ComboBox_tempChange(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure PythonInputOutput_hdc1080_SendData(Sender: TObject;
      const Data: AnsiString);
  private
    procedure DoPy_InitEngine;
  public
  end;

var
  Form_hdc1080: TForm_hdc1080;
  hdc: hdc1080Ob;
  hdc_attr: PyRecordOb;
  hdc_c:  hdc1080Ob_c;
  hdc_c_attr: PyRecordOb_c;
  Ob_hdc_c_attr: array[1..50] of PyRecordOb_c;
  ObI_hdc_attr: array[1..2] of PyRecordIOb;
  Ob_hdc_attr: array[1..50] of PyRecordOb;
  Ob_hdc_c: array[1..50] of hdc1080Ob_c;
  idx_hdc_attr,idx_hdc_c_attr,idx_hdc_c: integer;


implementation

{$R *.lfm}

uses hdc1080_read, hdc1080_write;

const
  cPyLibraryLinux = 'libpython3.7m.so.1.0';

procedure TForm_hdc1080.DoPy_InitEngine;
var
  S: string;
begin
  S:=
    {$ifdef linux} cPyLibraryLinux {$endif};
  PythonEngine_hdc1080.DllPath:= ExtractFileDir(S);
  PythonEngine_hdc1080.DllName:= ExtractFileName(S);
  PythonEngine_hdc1080.LoadDll;
end;

procedure TForm_hdc1080.FormCreate(Sender: TObject);
var
  i: Integer;
begin

  DoPy_InitEngine;

  hdc := hdc1080Ob.Init;
    for i in [1..50] do
    begin
    if i=1 then
       ObI_hdc_attr[1]:= PyRecordIOb.Init
     else
       Ob_hdc_attr[i]:= PyRecordOb.Init;

    Ob_hdc_c[i]:= hdc1080Ob_c.Init;
    Ob_hdc_c_attr[i]:=PyRecordOb_c.Init;
    end;

  idx_hdc_attr :=1;
  idx_hdc_c_attr :=1;
  idx_hdc_c :=1;

  read_hdc();
  read_measure();

end;

procedure TForm_hdc1080.ComboBox_tempChange(Sender: TObject);
var bit: String;
begin
  bit := IntToEnum (1,Form_hdc1080.ComboBox_temp.ItemIndex);   //temp accuracy button - new status
  hdc.attr1.attr_val_obj.attr2.attr_new_val := bit;
  hdc.attr1.attr_val_obj.attr2.attr_chg := true;
  Form_hdc1080.BitBtn_setting.ImageIndex := 1;
end;

procedure TForm_hdc1080.ComboBox_hmdtChange(Sender: TObject);
var bit: String;
begin
  bit := IntToEnum (0,Form_hdc1080.ComboBox_hmdt.ItemIndex);
  hdc.attr1.attr_val_obj.attr1.attr_new_val := bit;           //hmdt accuracy button - new status
  hdc.attr1.attr_val_obj.attr1.attr_chg := true;
  Form_hdc1080.BitBtn_setting.ImageIndex := 1;
end;

procedure TForm_hdc1080.ComboBox_modeChange(Sender: TObject);
var bit: String;
begin
  bit := IntToEnum_MODE (Form_hdc1080.ComboBox_mode.ItemIndex);
  hdc.attr1.attr_val_obj.attr4.attr_new_val := bit;          //mode button - new status
  hdc.attr1.attr_val_obj.attr4.attr_chg := true;
  Form_hdc1080.BitBtn_setting.ImageIndex := 1;
end;

procedure TForm_hdc1080.ComboBox_heatingChange(Sender: TObject);
var bit: String;
begin
  bit := IntToEnum_HEAT (Form_hdc1080.ComboBox_heating.ItemIndex);
  hdc.attr1.attr_val_obj.attr5.attr_new_val := bit;         //heat button - new status
  hdc.attr1.attr_val_obj.attr5.attr_chg := true;
  Form_hdc1080.BitBtn_setting.ImageIndex := 1;
end;

procedure TForm_hdc1080.BitBtn_settingClick(Sender: TObject);
begin
  write_conf_reg();
  read_hdc();
  read_measure();
  Form_hdc1080.BitBtn_setting.ImageIndex := 0;
end;


procedure TForm_hdc1080.PythonInputOutput_hdc1080_SendData(Sender: TObject;
  const Data: AnsiString);
begin

  hdc := StrToObj(data);

  case hdc.attr1.code_type of
   'READ_HDC':
     read_output_hdc(hdc);
   'READ_MEASURE':
     read_measure_hdc(hdc);
   'WRITE_REG_CONF':
     writeln('Success write to CONF Register');
    else
     exit;
    end;

end;

end.

