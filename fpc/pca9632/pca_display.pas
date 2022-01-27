unit pca_display;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls, Buttons,
  ComboEx, ComCtrls, ExtCtrls, Spin, Menus, Types, StrUtils, Math,
  pca_pyth_util, PythonEngine;

const
  TYPE0 = 0;
  TYPE1 = 1;
  PASSED = 0;
  FAILED = 1;

type

  { Tpca9632_main }

  Tpca9632_main = class(TForm)
    BitBtn1: TBitBtn;
    ComboBoxEx1: TComboBoxEx;
    ComboBoxEx10: TComboBoxEx;
    ComboBoxEx11: TComboBoxEx;
    ComboBoxEx12: TComboBoxEx;
    ComboBoxEx13: TComboBoxEx;
    ComboBoxEx2: TComboBoxEx;
    ComboBoxEx3: TComboBoxEx;
    ComboBoxEx4: TComboBoxEx;
    ComboBoxEx5: TComboBoxEx;
    ComboBoxEx6: TComboBoxEx;
    ComboBoxEx7: TComboBoxEx;
    ComboBoxEx8: TComboBoxEx;
    ComboBoxEx9: TComboBoxEx;
    Edit1: TEdit;
    Edit15: TEdit;
    Edit2: TEdit;
    Edit3: TEdit;
    Edit4: TEdit;
    Edit5: TEdit;
    Edit6: TEdit;
    Edit7: TEdit;
    Edit8: TEdit;
    Edit9: TEdit;
    Edit10: TEdit;
    Edit11: TEdit;
    Edit12: TEdit;
    Edit13: TEdit;
    Edit14: TEdit;
    GroupBox1: TGroupBox;
    ImageList1: TImageList;
    MainMenu1: TMainMenu;
    Creator: TMenuItem;
    Help: TMenuItem;
    PythonEngine1: TPythonEngine;
    PythonInputOutput1: TPythonInputOutput;
    Shape1,Shape2,Shape3,Shape4,Shape5: TShape;
    Shape6,Shape7,Shape8,Shape9: TShape;
    Shape10,Shape11,Shape12,Shape13: TShape;
    Shape14,Shape15,Shape16,Shape17,Shape18,Shape19: TShape;
    Shape20,Shape21,Shape22,Shape23: TShape;
    StaticText1: TStaticText;
    StaticText10: TStaticText;
    StaticText11: TStaticText;
    StaticText12: TStaticText;
    StaticText13: TStaticText;
    StaticText14: TStaticText;
    StaticText15: TStaticText;
    StaticText16: TStaticText;
    StaticText17: TStaticText;
    StaticText18: TStaticText;
    StaticText19: TStaticText;
    StaticText2: TStaticText;
    StaticText21: TStaticText;
    StaticText22: TStaticText;
    StaticText23: TStaticText;
    StaticText24: TStaticText;
    StaticText25: TStaticText;
    StaticText26: TStaticText;
    StaticText27: TStaticText;
    StaticText28: TStaticText;
    StaticText29: TStaticText;
    StaticText3: TStaticText;
    StaticText4: TStaticText;
    StaticText5: TStaticText;
    StaticText6: TStaticText;
    StaticText7: TStaticText;
    StaticText8: TStaticText;
    StaticText9: TStaticText;
    TrackBar1: TTrackBar;
    procedure BitBtn1Click(Sender: TObject);
    procedure ComboBoxEx10Change(Sender: TObject);
    procedure ComboBoxEx11Change(Sender: TObject);
    procedure ComboBoxEx12Change(Sender: TObject);
    procedure ComboBoxEx13Change(Sender: TObject);
    procedure ComboBoxEx1Change(Sender: TObject);
    procedure ComboBoxEx2Change(Sender: TObject);
    procedure ComboBoxEx3Change(Sender: TObject);
    procedure ComboBoxEx4Change(Sender: TObject);
    procedure ComboBoxEx5Change(Sender: TObject);
    procedure ComboBoxEx6Change(Sender: TObject);
    procedure ComboBoxEx7Change(Sender: TObject);
    procedure ComboBoxEx8Change(Sender: TObject);
    procedure ComboBoxEx9Change(Sender: TObject);
    procedure CreatorClick(Sender: TObject);
    procedure Edit1EditingDone(Sender: TObject);
    procedure Edit2EditingDone(Sender: TObject);
    procedure Edit3EditingDone(Sender: TObject);
    procedure Edit4EditingDone(Sender: TObject);
    procedure Edit5EditingDone(Sender: TObject);
    procedure Edit6EditingDone(Sender: TObject);
    procedure HelpClick(Sender: TObject);
    procedure PythonInputOutput1SendData(Sender: TObject; const Data: AnsiString);
    procedure Edit1Click(Sender: TObject);
    procedure Edit2Click(Sender: TObject);
    procedure Edit3Click(Sender: TObject);
    procedure Edit4Click(Sender: TObject);
    procedure Edit5Click(Sender: TObject);
    procedure Edit6Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure TrackBar1Change(Sender: TObject);
  private
  public
   procedure DoPy_InitEngine;
  end;

type
  TGWM = record
    value: Integer;
    perc: Real;
  end;

  TFREQ = record
    freq: Real;
    time: String[12];
  end;

GWM = Array [1 .. 65] of TGWM;
DIMM = Array [1 .. 17] of TGWM;
FREQ = Array [0 .. 256] of TFREQ;

var
  pca9632_main: Tpca9632_main;
  ItemEx010,ItemEx011,ItemEx012: TComboExItem;
  ItemEx020,ItemEx021,ItemEx022: TComboExItem;
  ItemEx030,ItemEx031,ItemEx032: TComboExItem;
  ItemEx040,ItemEx041,ItemEx042: TComboExItem;
  ItemEx050,ItemEx051,ItemEx052: TComboExItem;

  ItemEx060,ItemEx061,ItemEx062: TComboExItem;
  ItemEx070,ItemEx071,ItemEx072: TComboExItem;
  ItemEx080,ItemEx081,ItemEx082: TComboExItem;
  ItemEx090,ItemEx091,ItemEx092: TComboExItem;

  ItemEx100,ItemEx101,ItemEx102,ItemEx103,ItemEx104: TComboExItem;
  ItemEx110,ItemEx111,ItemEx112,ItemEx113,ItemEx114: TComboExItem;
  ItemEx120,ItemEx121,ItemEx122,ItemEx123,ItemEx124: TComboExItem;
  ItemEx130,ItemEx131,ItemEx132,ItemEx133,ItemEx134: TComboExItem;

  pca: pca6532Ob;
  pca_attr: PyRecordOb;
  pca_c:  pca6532Ob_c;
  pca_c_attr: PyRecordOb_c;
  Ob_pca_c_attr: array[1..50] of PyRecordOb_c;
  Ob_pca_attr: array[1..50] of PyRecordOb;
  Ob_pca_c: array[1..50] of pca6532Ob_c;
  grppwm: GWM;
  grpdim: DIMM;
  grpfreq: FREQ;
  test: Integer;

  procedure ComboBox_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
  procedure ComboBox_dmblnk_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
  procedure ComboBoxLdr_init (Item1, Item2, Item3, Item4: TComboExItem; ComboBoxEx: TComboBoxEx);
  function pwm_input_check (pwm_input: PChar): Real;
  function EnumToInt (Tp: Integer;S: String) : Integer;
  function IntToEnum (Tp: Integer;S: Integer) : String;
  function EnumToIntLdr (S: String) : Integer;
  function IntToEnumLdr (S: Integer) : String;

implementation

uses pca_grppwm,pca_read, pca_write, creator, help, missing_chip;

const
  cPyLibraryLinux = 'libpython3.9.so.1.0';

procedure ComboBox_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
begin
  {
  Item0 := ComboBoxEx.ItemsEx.Add;
  Item0.Caption:= '';
  Item0.Index:=2; }
  Item1 := ComboBoxEx.ItemsEx.Add;
  Item1.Caption:= '';
  Item1.ImageIndex:=0;
  Item1.Index:=0;
  Item2 := ComboBoxEx.ItemsEx.Add;
  Item2.Caption:= '';
  Item2.ImageIndex:=1;
  Item2.Index:=1;
end;

procedure ComboBox_dmblnk_init (Item1, Item2: TComboExItem; ComboBoxEx: TComboBoxEx);
begin
  {
  Item0 := ComboBoxEx.ItemsEx.Add;
  Item0.Caption:= '';
  Item0.Index:=2; }
  Item1 := ComboBoxEx.ItemsEx.Add;
  Item1.Caption:= '';
  Item1.ImageIndex:=4;
  Item1.Index:=0;
  Item2 := ComboBoxEx.ItemsEx.Add;
  Item2.Caption:= '';
  Item2.ImageIndex:=5;
  Item2.Index:=1;
end;

procedure ComboBoxLdr_init (Item1, Item2, Item3, Item4: TComboExItem; ComboBoxEx: TComboBoxEx);
begin
  Item1 := ComboBoxEx.ItemsEx.Add;
  Item1.Caption:= '';
  Item1.ImageIndex:=0;
  Item1.Index:=0;
  Item2 := ComboBoxEx.ItemsEx.Add;
  Item2.Caption:= '';
  Item2.ImageIndex:=1;
  Item2.Index:=1;
  Item3 := ComboBoxEx.ItemsEx.Add;
  Item3.Caption:= '';
  Item3.ImageIndex:=2;
  Item3.Index:=2;
  Item4 := ComboBoxEx.ItemsEx.Add;
  Item4.Caption:= '';
  Item4.ImageIndex:=3;
  Item4.Index:=3;
end;

function EnumToInt (Tp: Integer; S: String) : Integer;
begin
  if Tp = 0 then begin  // ON/OFF Type 0
    if S = 'ON'
      then Result := 0;
    if S = 'OFF'
      then Result := 1;
  end;
  if Tp = 1 then begin  // DIMMING/BLINKING Type 1
    if S = 'DIMMING'
      then Result := 0;
    if S = 'BLINKING'
      then Result := 1;
  end;
end;

function IntToEnum (Tp: Integer; S: Integer) : String;
begin
  if Tp = 0 then begin
    if S = 0
      then Result := 'ON';
    if S = 1
      then Result := 'OFF';
  end;
  if Tp = 1 then begin
    if S = 0
      then Result := 'DIMMING';
    if S = 1
      then Result := 'BLINKING';
  end;
end;

function EnumToIntLdr (S: String) : Integer;
begin
  if S = 'ON'
    then Result := 0;
  if S = 'OFF'
    then Result := 1;
  if S = 'PWM'
    then Result := 2;
  if S = 'PWM_GRPPWM'
    then Result := 3;
end;

function IntToEnumLdr (S: Integer) : String;
begin
  if S = 0
    then Result := 'ON';
  if S = 1
    then Result := 'OFF';
  if S = 2
    then Result := 'PWM';
  if S = 3
    then Result := 'GRP';
end;

{$R *.lfm}

{ Tpca9632_main }

function pwm_input_check (pwm_input: PChar): Real;
var
  filter: String;
  test_n: Real;
const
  ALLOWED = ['0'..'9',' ','.',','];
Function Valid: Boolean;
    var
      i: Integer;
    begin
      Result := Length(filter) > 0;
      i := 1;
      while Result and (i <= Length(filter)) do
      begin
        Result := Result AND (filter[i] in ALLOWED);
        inc(i);
      end;
      if  Length(filter) = 0 then Result := true;
end;
begin

  filter := StringReplace(pwm_input,' ','',[rfReplaceAll]);
  filter := StringReplace(filter,',','.',[rfReplaceAll]);

  if Valid then begin
    test_n := StrToFloat(filter);
    if (test_n <= 100) then
      Result := test_n
    else begin
      writeln('Number exceed 100');
      Result := -2;
    end;
  end
  else  begin
    writeln('Wrong Input please fix');
    Result := -1;
  end;
end;

procedure Tpca9632_main.PythonInputOutput1SendData(Sender: TObject;
  const Data: AnsiString);
begin

  pca := StrToObj(data);


  {
  write('ATTR3: ',pca.attr3.attr_name);
  write(':',pca.attr3.attr_val);
  writeln(); }


  case pca.attr1.code_type of
   'READ_PCA':
     read_output_pca(pca, grpdim, grpfreq);
   'READ_PCA_ERR':
     writeln('read_pca_err');
   'WRITE_REG_PCA_0':
      writeln('WRITE_REG_PCA correct');
   'WRITE_REG_PCA_1':
      writeln('WRITE_REG_PCA error');
   'WRITE_REG_PWM_0':
      writeln('WRITE_REG_PWM correct');
   'WRITE_REG_PWM_1':
      writeln('WRITE_REG_PWM error');
   'WRITE_REG_SGRPPWM_0':
      writeln('WRITE_REG_SEL_GRPPWM correct');
   'WRITE_REG_SGRPPWM_1':
      writeln('WRITE_REG_SEL_GPRPWM error');
   'WRITE_REG_GRPPWM_0':
      writeln('WRITE_REG_GRPPWM correct');
   'WRITE_REG_GRPPWM_1':
      writeln('WRITE_REG_GPRPWM error');
   'WRITE_REG_GRPFREQ_0':
      writeln('WRITE_REG_GRPFREQ correct');
   'WRITE_REG_GRPFREQ_1':
      writeln('WRITE_REG_GPRFREQ error');
   'TEST_PASSED':
     begin
       writeln('Selftest correct');
       test := PASSED;
     end;
   'MISSING_CHIP':
     begin
       writeln('Missed chip');
       test := FAILED;
       pca9632_main.Deactivate;
       Application.CreateForm(TForm_missing_chip, Form_missing_chip);
       Form_missing_chip.Visible:= True;
     end
    else
     exit;
    end;

end;

procedure Tpca9632_main.BitBtn1Click(Sender: TObject);
begin

  write_mode1_reg;
  write_mode2_reg;

  write_ledout_reg;
  read_pca;
end;

procedure Tpca9632_main.ComboBoxEx1Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx1.ItemIndex);
  write('ALLCALL: ',S);
  writeln();
  pca.attr1.attr_val_obj.attr1.attr_chg:=true;
  pca.attr1.attr_val_obj.attr1.attr_new_val:=S;
  Shape1.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx2Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx2.ItemIndex);
  write('SUB3: ',S);
  writeln();
  pca.attr1.attr_val_obj.attr2.attr_chg:=true;
  pca.attr1.attr_val_obj.attr2.attr_new_val:=S;
  Shape2.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx3Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx3.ItemIndex);
  write('SUB2: ',S);
  writeln();
  pca.attr1.attr_val_obj.attr3.attr_chg:=true;
  pca.attr1.attr_val_obj.attr3.attr_new_val:=S;
  Shape3.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx4Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx4.ItemIndex);
  write('SUB1: ',S);
  writeln();
  pca.attr1.attr_val_obj.attr4.attr_chg:=true;
  pca.attr1.attr_val_obj.attr4.attr_new_val:=S;
  Shape4.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx5Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx5.ItemIndex);
  write('SLEEP: ',S);
  writeln();
  pca.attr1.attr_val_obj.attr5.attr_chg:=true;
  pca.attr1.attr_val_obj.attr5.attr_new_val:=S;
  Shape5.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx6Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx6.ItemIndex);
  write('OUTDRV: ',S);
  writeln();
  pca.attr2.attr_val_obj.attr1.attr_chg:=true;
  pca.attr2.attr_val_obj.attr1.attr_new_val:=S;
  Shape6.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx7Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx7.ItemIndex);
  write('OCH: ',S);
  writeln();
  pca.attr2.attr_val_obj.attr2.attr_chg:=true;
  pca.attr2.attr_val_obj.attr2.attr_new_val:=S;
  Shape7.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx8Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE0,ComboBoxEx8.ItemIndex);
  write('INVRT: ',S);
  writeln();
  pca.attr2.attr_val_obj.attr3.attr_chg:=true;
  pca.attr2.attr_val_obj.attr3.attr_new_val:=S;
  Shape8.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx9Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnum(TYPE1,ComboBoxEx9.ItemIndex);
  write('DMBLNK: ',S);
  writeln();
  pca.attr2.attr_val_obj.attr4.attr_chg:=true;
  pca.attr2.attr_val_obj.attr4.attr_new_val:=S;
  Shape9.Visible:=True;
end;

procedure Tpca9632_main.CreatorClick(Sender: TObject);
begin
  Form_creator.Show;
end;

procedure Tpca9632_main.ComboBoxEx10Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnumLdr(ComboBoxEx10.ItemIndex);
  write('LDR0: ',S);
  writeln();
  pca.attr12.attr_val_obj.attr1.attr_chg:=true;
  pca.attr12.attr_val_obj.attr1.attr_new_val:=S;
  Shape20.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx11Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnumLdr(ComboBoxEx11.ItemIndex);
  write('LDR1: ',S);
  writeln();
  pca.attr12.attr_val_obj.attr2.attr_chg:=true;
  pca.attr12.attr_val_obj.attr2.attr_new_val:=S;
  Shape21.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx12Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnumLdr(ComboBoxEx12.ItemIndex);
  write('LDR2: ',S);
  writeln();
  pca.attr12.attr_val_obj.attr3.attr_chg:=true;
  pca.attr12.attr_val_obj.attr3.attr_new_val:=S;
  Shape22.Visible:=True;
end;

procedure Tpca9632_main.ComboBoxEx13Change(Sender: TObject);
var
  S: String;
begin
  S:=IntToEnumLdr(ComboBoxEx13.ItemIndex);
  write('LDR3: ',S);
  writeln();
  pca.attr12.attr_val_obj.attr4.attr_chg:=true;
  pca.attr12.attr_val_obj.attr4.attr_new_val:=S;
  Shape23.Visible:=True;
end;

procedure Tpca9632_main.DoPy_InitEngine;
var
  S: string;
begin
  S:=
    {$ifdef linux} cPyLibraryLinux {$endif};
  PythonEngine1.DllPath:= ExtractFileDir(S);
  PythonEngine1.DllName:= ExtractFileName(S);
  PythonEngine1.LoadDll;
end;

procedure Tpca9632_main.FormCreate(Sender: TObject);
begin

  DoPy_InitEngine;

  Edit11.Color:= clBlue;
  Edit11.Font.Color:=clWhite;
  Edit12.Color:= clBlue;
  Edit12.Font.Color:=clWhite;
  Edit13.Color:= clBlue;
  Edit13.Font.Color:=clWhite;
  Edit14.Color:= clBlue;
  Edit14.Font.Color:=clWhite;

  ComboBox_init (ItemEx011,ItemEx012,ComboBoxEx1);  // ALLCALL ON/OFF
  ComboBox_init (ItemEx021,ItemEx022,ComboBoxEx2);  // SUB3 ON/OFF
  ComboBox_init (ItemEx031,ItemEx032,ComboBoxEx3);  // SUB2 ON/OFF
  ComboBox_init (ItemEx041,ItemEx042,ComboBoxEx4);  // SUB1 ON/OFF
  ComboBox_init (ItemEx051,ItemEx052,ComboBoxEx5);  // SLEEP ON/OFF

  ComboBox_init (ItemEx061,ItemEx062,ComboBoxEx6);  // OUTDRV ON/OFF
  ComboBox_init (ItemEx071,ItemEx072,ComboBoxEx7);  // OCH ON/OFF
  ComboBox_init (ItemEx081,ItemEx082,ComboBoxEx8);  // INVRT ON/OFF
  ComboBox_dmblnk_init (ItemEx091,ItemEx092,ComboBoxEx9);  // DMBLNK DIMMING = 0 /BLINKING = 1

  ComboBoxLdr_init (ItemEx101,ItemEx102,ItemEx103,ItemEx104,ComboBoxEx10); // LDR0 ON/OFF/PWM/GRPPWM
  ComboBoxLdr_init (ItemEx111,ItemEx112,ItemEx113,ItemEx114,ComboBoxEx11); // LDR1 ON/OFF/PWM/GRPPWM
  ComboBoxLdr_init (ItemEx121,ItemEx122,ItemEx123,ItemEx124,ComboBoxEx12); // LDR2 ON/OFF/PWM/GRPPWM
  ComboBoxLdr_init (ItemEx131,ItemEx132,ItemEx133,ItemEx134,ComboBoxEx13); // LDR3 ON/OFF/PWM/GRPPWM

  grppwm := initialize_gwm;
  grpdim := initialize_dimming;
  grpfreq := initialize_freq;

  test := FAILED;

  self_test();
  if (test = 0) then
     begin
      Application.ShowMainForm := True;
      pca9632_main.Visible:= True;
      Application.CreateForm(TForm_creator, Form_creator);
      Application.CreateForm(TForm_help, Form_help);
      read_pca();
     end;

  //read_pca;

  //Image1.Stretch:= true;
  //Image1.Proportional:= true;
  //ImageList2.Draw(Image1.Picture.Bitmap.Canvas, 0, 0, 1);
  //ImageList2.GetBitmap(1,Image1.Picture.Bitmap);

end;

procedure Tpca9632_main.TrackBar1Change(Sender: TObject);
begin

end;

procedure Tpca9632_main.Edit1Click(Sender: TObject);
begin
  Edit1.ReadOnly:=false;
  Edit1.Color:=clWhite;
  Shape10.Visible:=True;
end;

procedure Tpca9632_main.Edit1EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  min,max: Real;
  pwm_value: String;
  cmd: TDict;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit1.GetTextBuf(in_buffer,Size);
  perc := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);
  pwm_value := IntToStr(round((perc*255)/100));

  if (pca.attr12.attr_val_obj.attr1.attr_val = 'PWM') or
    ((pca.attr12.attr_val_obj.attr1.attr_val = 'PWM_GRPPWM') and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING')) then begin
    cmd.key := 'PWM';
    cmd.kval := pwm_value;

    write_pwm_reg_pca('PWM0',cmd);
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edi): ',Edit1.Text);
    write('PWM0(PWM): ',Edit1.Text);
    writeln();
    end
  else
    if pca.attr12.attr_val_obj.attr1.attr_val = 'PWM_GRPPWM' then
      begin
      cmd.key := 'SGRPPWM';
      cmd.kval := pwm_value;

      for i:= 1 to 64 do
        begin
        min := abs(grppwm[i].value - StrToInt(cmd.kval));
        if min <= 3 then
          begin
           max := abs(grppwm[i+1].value - StrToInt(cmd.kval));
           if min < max then cmd.kval := IntToStr(grppwm[i].value)
            else cmd.kval := IntToStr(grppwm[i+1].value);
           write_pwm_reg_pca('PWM0',cmd);
           break;
          end
        else continue;
       end;
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edit1.Text;
    write('PWM0(GRPPWM): ',Edit1.Text);
    writeln();
     end;

  Edit1.Color:=clMenubar;
  Shape10.Visible:=false;
  Edit1.ReadOnly:=true;

  read_pca;

end;

procedure Tpca9632_main.Edit2Click(Sender: TObject);
begin
  Edit2.ReadOnly:=false;
  Edit2.Color:=clWhite;
  Shape11.Visible:=True;
end;

procedure Tpca9632_main.Edit2EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  min,max: Real;
  pwm_value: String;
  cmd: TDict;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit2.GetTextBuf(in_buffer,Size);
  perc := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);
  pwm_value := IntToStr(round((perc*255)/100));

  if (pca.attr12.attr_val_obj.attr2.attr_val = 'PWM') or
    ((pca.attr12.attr_val_obj.attr2.attr_val = 'PWM_GRPPWM') and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING')) then begin
    cmd.key := 'PWM';
    cmd.kval := pwm_value;

    write_pwm_reg_pca('PWM1',cmd);
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edi): ',Edit1.Text);
    write('PWM1(PWM): ',Edit2.Text);
    writeln();
    end
  else
    if pca.attr12.attr_val_obj.attr2.attr_val = 'PWM_GRPPWM' then
      begin
      cmd.key := 'SGRPPWM';
      cmd.kval := pwm_value;

      for i:= 1 to 64 do
        begin
        min := abs(grppwm[i].value - StrToInt(cmd.kval));
        if min <= 3 then
          begin
           max := abs(grppwm[i+1].value - StrToInt(cmd.kval));
           if min < max then cmd.kval := IntToStr(grppwm[i].value)
            else cmd.kval := IntToStr(grppwm[i+1].value);
           write_pwm_reg_pca('PWM1',cmd);
           break;
          end
        else continue;
       end;
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edit1.Text;
    write('PWM1(GRPPWM): ',Edit2.Text);
    writeln();
     end;

  Edit2.Color:=clMenubar;
  Shape11.Visible:=false;
  Edit2.ReadOnly:=true;

  read_pca;

end;

procedure Tpca9632_main.Edit3Click(Sender: TObject);
begin
  Edit3.ReadOnly:=false;
  Edit3.Color:=clWhite;
  Shape12.Visible:=True;
end;

procedure Tpca9632_main.Edit3EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  min,max: Real;
  pwm_value: String;
  cmd: TDict;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit3.GetTextBuf(in_buffer,Size);
  perc := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);
  pwm_value := IntToStr(round((perc*255)/100));

  if (pca.attr12.attr_val_obj.attr3.attr_val = 'PWM') or
    ((pca.attr12.attr_val_obj.attr3.attr_val = 'PWM_GRPPWM') and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING')) then begin
    cmd.key := 'PWM';
    cmd.kval := pwm_value;

    write_pwm_reg_pca('PWM2',cmd);
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edi): ',Edit1.Text);
    write('PWM2(PWM): ',Edit3.Text);
    writeln();
    end
  else
    if pca.attr12.attr_val_obj.attr3.attr_val = 'PWM_GRPPWM' then
      begin
      cmd.key := 'SGRPPWM';
      cmd.kval := pwm_value;

      for i:= 1 to 64 do
        begin
        min := abs(grppwm[i].value - StrToInt(cmd.kval));
        if min <= 3 then
          begin
           max := abs(grppwm[i+1].value - StrToInt(cmd.kval));
           if min < max then cmd.kval := IntToStr(grppwm[i].value)
            else cmd.kval := IntToStr(grppwm[i+1].value);
           write_pwm_reg_pca('PWM2',cmd);
           break;
          end
        else continue;
       end;
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edit1.Text;
    write('PWM2(GRPPWM): ',Edit3.Text);
    writeln();
     end;

  Edit3.Color:=clMenubar;
  Shape12.Visible:=false;
  Edit3.ReadOnly:=true;

  read_pca;

end;

procedure Tpca9632_main.Edit4Click(Sender: TObject);
begin
  Edit4.ReadOnly:=false;
  Edit4.Color:=clWhite;
  Shape13.Visible:=True;
end;

procedure Tpca9632_main.Edit4EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  min,max: Real;
  pwm_value: String;
  cmd: TDict;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit4.GetTextBuf(in_buffer,Size);
  perc := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);
  pwm_value := IntToStr(round((perc*255)/100));

  if (pca.attr12.attr_val_obj.attr4.attr_val = 'PWM') or
    ((pca.attr12.attr_val_obj.attr4.attr_val = 'PWM_GRPPWM') and (pca.attr2.attr_val_obj.attr4.attr_val = 'BLINKING')) then begin
    cmd.key := 'PWM';
    cmd.kval := pwm_value;

    write_pwm_reg_pca('PWM3',cmd);
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edi): ',Edit1.Text);
    write('PWM3(PWM): ',Edit4.Text);
    writeln();
    end
  else
    if pca.attr12.attr_val_obj.attr4.attr_val = 'PWM_GRPPWM' then
      begin
      cmd.key := 'SGRPPWM';
      cmd.kval := pwm_value;

      for i:= 1 to 64 do
        begin
        min := abs(grppwm[i].value - StrToInt(cmd.kval));
        if min <= 3 then
          begin
           max := abs(grppwm[i+1].value - StrToInt(cmd.kval));
           if min < max then cmd.kval := IntToStr(grppwm[i].value)
            else cmd.kval := IntToStr(grppwm[i+1].value);
           write_pwm_reg_pca('PWM3',cmd);
           break;
          end
        else continue;
       end;
    //pca.attr3.attr_chg:=true;
    //pca.attr3.attr_new_val:=Edit1.Text;
    write('PWM3(GRPPWM): ',Edit4.Text);
    writeln();
     end;

  Edit4.Color:=clMenubar;
  Shape13.Visible:=false;
  Edit4.ReadOnly:=true;

  read_pca;

end;

procedure Tpca9632_main.Edit5Click(Sender: TObject);
begin
  Edit5.ReadOnly:=false;
  Edit5.Color:=clWhite;
  Shape14.Visible:=True;
end;

procedure Tpca9632_main.Edit5EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  high,low: Real;
  cmd: TDict;
  value: Real;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit5.GetTextBuf(in_buffer,Size);
  value := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);

  cmd.key := 'GRPPWM';

  if (value >= 0) and (value <= 100) then begin
  if  (pca.attr2.attr_val_obj.attr4.attr_val = 'DIMMING' ) then
    for i:= 1 to 16 do
    begin
    high := grpdim[i].perc - value;
    low := grpdim[i+1].perc - value;
    if (high <= 0) and (low >= 0) then
      begin
      cmd.kval := IntToStr(grpdim[i].value);
      write_pwm_reg_pca('GRPPWM',cmd);
      writeln('GRPPWM(DIMMING): ',Edit5.Text);
      break;
      end
      else continue;
    end
  else
    if grpfreq[StrToInt(pca.attr8.attr_val)].freq >= 6 then
     for i:=1 to 64 do
      begin
      high := grppwm[i].perc - value;
      low := grppwm[i+1].perc - value;
      if (high <= 0) and (low >= 0) then
        begin
        cmd.kval := IntToStr(grppwm[i].value);
        write_pwm_reg_pca('GRPPWM',cmd);
        writeln('GRPPWM(BLINKING <= 6Hz): ',Edit5.Text);
        break;
        end
       else continue
       end
    else
     begin
       cmd.kval := IntToStr(round((value*255)/100));
       write_pwm_reg_pca('GRPPWM',cmd);
       writeln('GRPPWM(BLINKING > 6Hz): ',Edit5.Text);
      end;

    Edit5.Color:=clMenubar;
    Shape14.Visible:=false;
    Edit5.ReadOnly:=true;
    read_pca;
  end
  else
    writeln('GRPPWM: not in 0 .. 100%');

end;

procedure Tpca9632_main.Edit6Click(Sender: TObject);
begin
  Edit6.ReadOnly:=false;
  Edit6.Color:=clWhite;
  Shape15.Visible:=True;
end;

procedure Tpca9632_main.Edit6EditingDone(Sender: TObject);
var
  in_buffer: PChar;
  Size: Byte;
  perc: Real;
  high,low: Real;
  cmd: TDict;
  value: Real;
  i: Integer;
begin
  Size := 20;
  GetMem(in_buffer, Size);
  Edit6.GetTextBuf(in_buffer,Size);
  value := pwm_input_check (in_buffer);
  FreeMem(in_buffer, Size);

  cmd.key := 'GRPFREQ';

  if (value >= 0.0938) and (value <= 24) then begin
    for i:= 0 to 256 do
    begin
    high := grpfreq[i].freq - value;
    low := grpfreq[i+1].freq - value;
    if (high >= 0) and (low <= 0) then
      begin
      cmd.kval := IntToStr(i);
      write_pwm_reg_pca('GRPFREQ',cmd);
      break;
      end
      else continue;
    end;

    write('GRPFREQ: ',Edit6.Text);
    writeln();

    Edit6.Color:=clMenubar;
    Shape15.Visible:=false;
    Edit6.ReadOnly:=true;
    read_pca;
  end
  else
    writeln('GRPFREQ: not in 24 .. 0.0938 Hz');

end;

procedure Tpca9632_main.HelpClick(Sender: TObject);
begin
  Form_help.Show;
end;

end.

