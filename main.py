import discord
from discord.ext import commands
from discord import app_commands

TOKEN = 'MTQ5NDU5OTc5NjI1MjQ3OTU1OA.GrJxhH.zL6SULg-QWwt2O_vtcNpjddXraY9PR3-9vJ9pY'

# كود زر الإغلاق
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="إغلاق التذكرة 🔒", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("سيتم إغلاق التذكرة خلال 5 ثوانٍ...")
        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="اختر نوع التذكرة...",
        options=[
            discord.SelectOption(label="استفسار", emoji="❓"),
            discord.SelectOption(label="شراء ملفات", emoji="📁"),
            discord.SelectOption(label="شراء سكريبت", emoji="📜"),
            discord.SelectOption(label="شراء بوت", emoji="🤖"),
        ],
        custom_id="ticket_select"
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        guild = interaction.guild
        user = interaction.user
        choice = select.values[0]

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        channel = await guild.create_text_channel(name=f"{choice}-{user.name}", overwrites=overwrites)
        await interaction.response.send_message(f"تم فتح تذكرة {choice} هنا: {channel.mention}", ephemeral=True)
        
        # رسالة داخل التيكت مع زر الإغلاق
        embed = discord.Embed(title=f"تذكرة: {choice}", description=f"أهلاً {user.mention}، كيف يمكننا مساعدتك؟\n\nاضغط على الزر أدناه لإغلاق التذكرة.", color=discord.Color.green())
        await channel.send(embed=embed, view=CloseView())

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(TicketView())
        self.add_view(CloseView()) # تفعيل زر الإغلاق

bot = MyBot()

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(title="مركز الدعم الفني 🛠️", description="اختر القسم المطلوب من القائمة أدناه لفتح تذكرة.", color=discord.Color.blue())
    await ctx.send(embed=embed, view=TicketView())

bot.run(TOKEN)