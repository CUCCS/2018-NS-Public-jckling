.class public Lcn/edu/cuc/misdemo/MainActivity;
.super Landroid/support/v7/app/AppCompatActivity;
.source "MainActivity.java"


# static fields
.field public static final EXTRA_MESSAGE:Ljava/lang/String; = "cn.edu.cuc.mishello.MESSAGE"


# instance fields
.field public sharedPreferences:Landroid/content/SharedPreferences;


# direct methods
.method public constructor <init>()V
    .locals 0

    .line 15
    invoke-direct {p0}, Landroid/support/v7/app/AppCompatActivity;-><init>()V

    return-void
.end method


# virtual methods
.method protected onCreate(Landroid/os/Bundle;)V
    .locals 2

    .line 24
    invoke-super {p0, p1}, Landroid/support/v7/app/AppCompatActivity;->onCreate(Landroid/os/Bundle;)V

    const p1, 0x7f09001d

    .line 25
    invoke-virtual {p0, p1}, Lcn/edu/cuc/misdemo/MainActivity;->setContentView(I)V

    const p1, 0x7f0b002a

    .line 28
    invoke-virtual {p0, p1}, Lcn/edu/cuc/misdemo/MainActivity;->getString(I)Ljava/lang/String;

    move-result-object p1

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0}, Lcn/edu/cuc/misdemo/MainActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object p1

    iput-object p1, p0, Lcn/edu/cuc/misdemo/MainActivity;->sharedPreferences:Landroid/content/SharedPreferences;

    .line 29
    iget-object p1, p0, Lcn/edu/cuc/misdemo/MainActivity;->sharedPreferences:Landroid/content/SharedPreferences;

    const v0, 0x7f0b002b

    invoke-virtual {p0, v0}, Lcn/edu/cuc/misdemo/MainActivity;->getString(I)Ljava/lang/String;

    move-result-object v0

    const-string v1, ""

    invoke-interface {p1, v0, v1}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;

    move-result-object p1

    const v0, 0x7f070036

    .line 30
    invoke-virtual {p0, v0}, Lcn/edu/cuc/misdemo/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v0

    check-cast v0, Landroid/widget/EditText;

    .line 31
    invoke-virtual {v0, p1}, Landroid/widget/EditText;->setText(Ljava/lang/CharSequence;)V

    return-void
.end method

.method public sendMessage(Landroid/view/View;)V
    .locals 3

    const p1, 0x7f0b002a

    .line 66
    invoke-virtual {p0, p1}, Lcn/edu/cuc/misdemo/MainActivity;->getString(I)Ljava/lang/String;

    move-result-object p1

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0}, Lcn/edu/cuc/misdemo/MainActivity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;

    move-result-object p1

    iput-object p1, p0, Lcn/edu/cuc/misdemo/MainActivity;->sharedPreferences:Landroid/content/SharedPreferences;

    .line 67
    iget-object p1, p0, Lcn/edu/cuc/misdemo/MainActivity;->sharedPreferences:Landroid/content/SharedPreferences;

    invoke-interface {p1}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;

    move-result-object p1

    .line 70
    new-instance v0, Landroid/content/Intent;

    const-class v1, Lcn/edu/cuc/misdemo/DisplayMessageActivity;

    invoke-direct {v0, p0, v1}, Landroid/content/Intent;-><init>(Landroid/content/Context;Ljava/lang/Class;)V

    const v1, 0x7f070036

    .line 71
    invoke-virtual {p0, v1}, Lcn/edu/cuc/misdemo/MainActivity;->findViewById(I)Landroid/view/View;

    move-result-object v1

    check-cast v1, Landroid/widget/EditText;

    .line 72
    invoke-virtual {v1}, Landroid/widget/EditText;->getText()Landroid/text/Editable;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    const-string v2, "cn.edu.cuc.mishello.MESSAGE"

    .line 73
    invoke-virtual {v0, v2, v1}, Landroid/content/Intent;->putExtra(Ljava/lang/String;Ljava/lang/String;)Landroid/content/Intent;

    const v2, 0x7f0b002b

    .line 76
    invoke-virtual {p0, v2}, Lcn/edu/cuc/misdemo/MainActivity;->getString(I)Ljava/lang/String;

    move-result-object v2

    invoke-interface {p1, v2, v1}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;

    .line 77
    invoke-interface {p1}, Landroid/content/SharedPreferences$Editor;->commit()Z

    .line 79
    invoke-virtual {p0, v0}, Lcn/edu/cuc/misdemo/MainActivity;->startActivity(Landroid/content/Intent;)V

    return-void
.end method
