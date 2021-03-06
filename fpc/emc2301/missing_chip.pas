unit missing_chip;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, StdCtrls,
  ExtCtrls;

type

  { TForm_missing_chip }

  TForm_missing_chip = class(TForm)
    Image1: TImage;
    Timer1: TTimer;
    StaticText1: TStaticText;
    procedure FormCreate(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
  private
    Completed: Boolean;
  public

  end;

var
  Form_missing_chip: TForm_missing_chip;

implementation

{$R *.lfm}

{ TForm_missing_chip }

procedure TForm_missing_chip.FormCreate(Sender: TObject);
begin
  Completed := False;
  //writeln('missing form create');
  Timer1.Interval := 20000; // 10s minimum time to show splash screen
  Timer1.Enabled := True;
end;

procedure TForm_missing_chip.Timer1Timer(Sender: TObject);
begin
  Timer1.Enabled := False;
  Form_missing_chip.Hide;
  Completed := True;
  Application.Terminate;
  Halt;
end;

end.

