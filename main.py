import discord
from discord.ext import commands
import asyncio

# إعدادات البوت الأساسية
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 1. كلاس زر إغلاق التذكرة (يظهر داخل التذكرة المفتوحة)
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="إغلاق التذكرة | Close", style=discord.ButtonStyle.red, custom_id="close_btn")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("سيتم حذف هذه التذكرة خلال 5 ثوانٍ...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

# 2. كلاس القائمة المنسدلة (بناءً على صورتك)
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="استفسار - Ask", value="ask", emoji="📩"),
            discord.SelectOption(label="المتجر - Store", value="store", emoji="💸"),
            discord.SelectOption(label="تذكرة باند - Banned Ticket", value="banned", emoji="⛔"),
            discord.SelectOption(label="باند حماية - Security", value="security", emoji="🛡️"),
            discord.SelectOption(label="طلب تعويض - Compensation", value="compensation", emoji="💰"),
        ]
        super().__init__(placeholder="...اختر نوع التذكرة من هنا", options=options, custom_id="ticket_dropdown")

    async def callback(self, interaction: discord.Interaction):
        # التحقق من وجود تذكرة سابقة لمنع التكرار (سبام)
        ticket_name = f"ticket-{interaction.user.name.lower()}"
        existing_channel = discord.utils.get(interaction.guild.channels, name=ticket_name)
        
        if existing_channel:
            return await interaction.response.send_message(f"لديك تذكرة مفتوحة بالفعل هنا: {existing_channel.mention}", ephemeral=True)

        # إعدادات صلاحيات القناة (صاحب التذكرة فقط يراها)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # إنشاء القناة
        channel = await interaction.guild.create_text_channel(name=ticket_name, overwrites=overwrites)
        
        await interaction.response.send_message(f"تم إنشاء تذكرتك بنجاح: {channel.mention}", ephemeral=True)
        
        # رسالة الترحيب داخل التذكرة
        embed = discord.Embed(
            title="تذكرة جديدة",
            description=f"أهلاً بك {interaction.user.mention} في قسم **{self.values[0]}**.\nيرجى طرح موضوعك وسيقوم الإداري بالرد عليك قريباً.",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed, view=CloseTicketView())

# 3. الـ View الذي يجمع القائمة
class TicketMainView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# 4. أمر إنشاء رسالة التذاكر الأساسية (اكتب !setup في الشات)
@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="📩 فتح تذكرة | Open Ticket",
        description=(
            "**قوانين التذكرة:**\n\n"
            "1️⃣ في حال عدم الرد خلال 12 ساعة سيتم إغلاق التكت\n"
            "2️⃣ أي شكوى أو طلب تعويض بدون دليل مرفوضة\n"
            "3️⃣ ممنوع تفتح تكت و ما ترد فيها\n"
            "4️⃣ الرجاء اختيار نوع التذكرة حتى تقدر الادارة مساعدتك بسرعة\n"
            "5️⃣ في حال فتحت تذكرة ولم تكتب شيء خلال ساعة سيتم اغلاق التذكرة\n"
            "6️⃣ يمنع فتح تذكرتين بنفس الموضوع منعاً باتاً\n"
            "7️⃣ اشرح موضوعك ولا تنتظر رد الإداري عليك\n"
            "8️⃣ يمنع السبام في التكتات"
        ),
        color=discord.Color.from_rgb(47, 49, 54) # لون غامق قريب للصورة
    )
    await ctx.send(embed=embed, view=TicketMainView())

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is ready!')
    # لضمان بقاء الأزرار تعمل بعد إعادة تشغيل البوت
    bot.add_view(TicketMainView())
    bot.add_view(CloseTicketView())

bot.run("MTQ5MTc1NDQxNjY1NzkyNDI3OA.Gb_s7Y.QocG7a2on6CwiIsNtab21Zo_i7tLXtEAl21LqY")
